#!/usr/bin/env python
"""
Updates offsets and lengths in a simple PDF file.

The PDF specification requires that the xref section at the end
of a PDF file has the correct offsets to the PDF's objects.
It further requires that the dictionary of a stream object
contains a /Length-entry giving the length of the encoded stream.

When editing a PDF file using a text-editor (e.g. vim) it is
elaborate to compute or adjust these offsets and lengths.

This command tries to compute /Length-entries of the stream dictionaries
and the offsets in the xref-section automatically.

It expects that the PDF file has ASCII encoding only. It may
use ISO-8859-1 or UTF-8 in its comments.
Therefore it expects that there a no binary streams.
It expects that there is one xref-section only.
It expects that the /Length-entries have default values containing
enough digits, e.g. /Length 000 when the stream consists of 576 bytes.

EXAMPLE
   offset-updater -v --encoding UTF-8 issue-297.pdf issue-297.out.pdf
"""

from collections.abc import Iterable
from pathlib import Path
import logging
import re
import sys


def update_lines(linesIn: Iterable[str], encoding: str) -> Iterable[str]:
    """Iterates over the lines of a pdf-files and updates offsets.

    The input is expected to be a pdf without binary-sections.

    :param linesIn: An Iterable over the lines including line-breaks.
    :param encoding: The encoding, e.g. "iso-8859-1" or "UTF-8".
    :return The output is a list of lines to be written in the given encoding.
    """
    logger = logging.getLogger("update_lines")
    regExpObj = re.compile(r"^([0-9]+) ([0-9]+) obj *")
    regExpContent = re.compile(r"^(.*)")
    regExpLength = re.compile(r"^(.*/Length )([0-9]+)( .*)", re.DOTALL)

    linesOut = []  # lines to be written
    mapOffsets = {}  # map from line-number to offset
    mapObjOffset = {}  # map from object-number to offset
    lineNo = 0  # current line-number (starting at 0)
    offsetOut = 0  # current offset in output-file
    lineXref = None  # line-number of xref-line (in xref-section only)
    lineStartxref = None  # line-number of startxref-line
    currentObj = None  # number of current object
    currentLengthLine = None  # line containing stream-length
    lenStream = None  # length of stream (in stream only)
    mapStreamLen = {}  # map from object-number to length /Length of stream
    mapObjLengthLine = {}  # map from object-number to /Length-line
    mapObjLengthLineNo = {}  # map from object-number to lineNo of /Length-line
    for line in linesIn:
        lineNo += 1
        mContent = regExpContent.match(line)
        if mContent is None:
            raise RuntimeError(f"Line {lineNo} without line-break.")
        content = mContent.group(1)
        mapOffsets[lineNo] = offsetOut
        mObj = regExpObj.match(line)
        if mObj is not None:
            currentObj = mObj.group(1)
            logger.info(f"line {lineNo}: object {currentObj}")
            mapObjOffset[currentObj] = int(offsetOut)
        if content == "xref":
            offsetXref = offsetOut
            lineXref = lineNo
        elif content == "startxref":
            lineStartxref = lineNo
            lineXref = None
        elif content == "stream":
            logger.info(f"line {lineNo}: start stream")
            lenStream = 0
        elif content == "endstream":
            logger.info(f"line {lineNo}: end stream")
            if currentObj is None:
                raise RuntimeError(
                    f"Line {lineNo}: " + "endstream without object-start."
                )
            if lenStream is None:
                raise RuntimeError(f"Line {lineNo}: endstream without stream.")
            logger.info(f"line {lineNo}: /Length {lenStream}")
            mapStreamLen[currentObj] = lenStream
        elif content == "endobj":
            currentObj = None
        elif currentObj is not None and lenStream is None:
            mLength = regExpLength.match(line)
            if mLength is not None:
                logger.info(f"line {lineNo}, /Length: {content}")
                mapObjLengthLine[currentObj] = line
                mapObjLengthLineNo[currentObj] = lineNo
        elif currentObj is not None and lenStream is not None:
            lenStream += len(line.encode(encoding))
        elif lineXref is not None and lineNo > lineXref + 2:
            objNo = lineNo - lineXref - 2
            if objNo <= len(mapObjOffset) and str(objNo) in mapObjOffset:
                eol = line[-2:]
                xrefUpd = ("%010d" % mapObjOffset[str(objNo)]) + " 00000 n"
                logger.info(f"{content} -> {xrefUpd}")
                line = xrefUpd + eol
        elif lineStartxref is not None and lineNo == lineStartxref + 1:
            line = "%d\n" % offsetXref
        linesOut.append(line)

        offsetOut += len(line.encode(encoding))

    for currentObj, streamLen in mapStreamLen.items():
        if not currentObj in mapObjLengthLine:
            raise RuntimeError(
                f"obj {currentObj} with stream-len {len}"
                + f" has no object-length-line: {mapObjLengthLine}"
            )
        mLength = regExpLength.match(mapObjLengthLine[currentObj])
        lenDigits = len(mLength.group(2))
        lenFormat = "%%0%dd" % lenDigits
        sStreamLen = lenFormat % streamLen
        if len(sStreamLen) > lenDigits:
            raise RuntimeError(
                f"Not enough digits in /Length-entry {mLength.group(2)}"
                + f" of object {currentObj}:"
                + f" too short to take /Length {sStreamLen}"
            )
        line = mLength.group(1) + sStreamLen + mLength.group(3)
        linesOut[mapObjLengthLineNo[currentObj] - 1] = line

    return linesOut


def main(file_in: Path, file_out: Path, encoding: str, verbose: bool) -> None:
    if verbose:
        logging.basicConfig(level=logging.INFO)
        print(f"Read {file_in}")

    with open(file_in, "r") as f:
        linesOut = update_lines(f, encoding)

    with open(file_out, "wb") as f:
        for line in linesOut:
            f.write(line.encode(encoding))

    if verbose:
        print(f"Wrote {file_out}")
