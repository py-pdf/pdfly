"""
Extract images from PDF without resampling or altering.

Adapted from work by Sylvain Pelissier
http://stackoverflow.com/questions/2693820/extract-images-from-pdf-without-resampling-in-python
"""

from pathlib import Path

import PyPDF2
from PIL import Image


def main(pdf: Path) -> None:
    reader = PyPDF2.PdfFileReader(open(pdf, "rb"))
    page0 = reader.pages[30]

    if "/XObject" in page0["/Resources"]:
        x_object = page0["/Resources"]["/XObject"].getObject()

        for obj in x_object:
            if x_object[obj]["/Subtype"] == "/Image":
                size = (x_object[obj]["/Width"], x_object[obj]["/Height"])
                data = x_object[obj].getData()
                if x_object[obj]["/ColorSpace"] == "/DeviceRGB":
                    mode = "RGB"
                else:
                    mode = "P"

                if "/Filter" in x_object[obj]:
                    if x_object[obj]["/Filter"] == "/FlateDecode":
                        img = Image.frombytes(mode, size, data)
                        if "/SMask" in x_object[obj]:  # add alpha channel
                            alpha = Image.frombytes(
                                "L", size, x_object[obj]["/SMask"].getData()
                            )
                            img.putalpha(alpha)
                        img.save(obj[1:] + ".png")
                    elif x_object[obj]["/Filter"] == "/DCTDecode":
                        img = open(obj[1:] + ".jpg", "wb")
                        img.write(data)
                        img.close()
                    elif x_object[obj]["/Filter"] == "/JPXDecode":
                        img = open(obj[1:] + ".jp2", "wb")
                        img.write(data)
                        img.close()
                    elif x_object[obj]["/Filter"] == "/CCITTFaxDecode":
                        img = open(obj[1:] + ".tiff", "wb")
                        img.write(data)
                        img.close()
                else:
                    img = Image.frombytes(mode, size, data)
                    img.save(obj[1:] + ".png")
    else:
        print("No image found.")
