"""
Updates offsets and lengths in a simple PDF file.

The PDF specification requires that the xref section at the end
of a PDF file has the correct offsets of the PDF's objects.
It further requires that the dictionary of a stream object
contains a /Length-entry giving the length of the encoded stream.

When editing a PDF file using a text-editor (e.g. vim) it is
elaborate to compute or adjust these offsets and lengths.

This command tries to compute /Length-entries of the stream dictionaries
and the offsets in the xref-section automatically.

It expects that the PDF file has ASCII encoding only. It may
use ISO-8859-1 or UTF-8 in its comments.
The current implementation incorrectly replaces CR (0x0d) by LF (0x0a) in binary data.
It expects that there is one xref-section only.
It expects that the /Length-entries have default values containing
enough digits, e.g. /Length 000 when the stream consists of 576 bytes.

Example:
   update-offsets --verbose --encoding ISO-8859-1 issue-297.pdf issue-297.out.pdf

"""

import re
from pathlib import Path

from rich.console import Console

# Here, only simple regular expressions are used.
# Beyond a certain level of complexity, switching to a proper PDF dictionary parser would be better.
RE_OBJ = re.compile(r"^([0-9]+) ([0-9]+) obj *")
RE_CONTENT = re.compile(r"^([^\r\n]*)", re.DOTALL)
RE_LENGTH_REF = re.compile(r"^(.*/Length )([0-9]+) ([0-9]+) R(.*)", re.DOTALL)
RE_LENGTH = re.compile(
    r"^(.*/Length )([0-9]+)([ />\x00\t\f\r\n].*)", re.DOTALL
)


def update_lines(
    lines_in: list[str], encoding: str, console: Console, verbose: bool
) -> list[str]:
    """
    Iterates over the lines of a pdf-files and updates offsets.

    The input is expected to be a pdf without binary-sections.

    :param lines_in: A list over the lines including line-breaks.
    :param encoding: The encoding, e.g. "iso-8859-1" or "UTF-8".
    :param console: Console used to print messages.
    :param verbose: True to activate logging of info-messages.
    :return The output is a list of lines to be written
            in the given encoding.
    """
    lines_out = []  # lines to be written
    map_line_offset = {}  # map from line-number to offset
    map_obj_offset = {}  # map from object-number to offset
    map_obj_line = {}  # map from object-number to line-number
    line_no = 0  # current line-number (starting at 0)
    offset_out = 0  # current offset in output-file
    line_xref = None  # line-number of xref-line (in xref-section only)
    line_startxref = None  # line-number of startxref-line
    curr_obj = None  # number of current object
    len_stream = None  # length of stream (in stream only)
    offset_xref = None  # offset of xref-section
    map_stream_len = {}  # map from object-number to /Length of stream
    map_obj_length_line = {}  # map from object-number to /Length-line
    map_obj_length_ref = (
        {}
    )  # map from object-number to /Length-reference (e.g. "3")
    map_obj_length_line_no = {}  # map from object-number to line_no of length
    # of /Length-line
    for idx, line in enumerate(lines_in):
        line_no = idx + 1
        m_content = RE_CONTENT.match(line)
        if m_content is None:
            raise RuntimeError(
                f"Invalid PDF file: line {line_no} without line-break."
            )
        content = m_content.group(1)
        map_line_offset[line_no] = offset_out
        m_obj = RE_OBJ.match(line)
        if m_obj is not None:
            curr_obj = m_obj.group(1)
            curr_gen = m_obj.group(2)
            if verbose:
                console.print(f"line {line_no}: object {curr_obj}")
            if curr_gen != "0":
                raise RuntimeError(
                    f"Invalid PDF file: generation {curr_gen} of object {curr_obj} in line {line_no} is not supported."
                )
            map_obj_offset[curr_obj] = int(offset_out)
            map_obj_line[curr_obj] = line_no
            len_stream = None

        if content == "xref":
            offset_xref = offset_out
            line_xref = line_no
        elif content == "startxref":
            line_startxref = line_no
            line_xref = None
        elif content == "stream":
            if verbose:
                console.print(f"line {line_no}: start stream")
            len_stream = 0
        elif content == "endstream":
            if verbose:
                console.print(f"line {line_no}: end stream")
            if curr_obj is None:
                raise RuntimeError(
                    f"Invalid PDF file: line {line_no}: endstream without object-start."
                )
            if len_stream is None:
                raise RuntimeError(
                    f"Invalid PDF file: line {line_no}: endstream without stream."
                )
            if len_stream > 0:
                # Ignore the last EOL
                len_stream = (
                    len_stream - 2
                    if lines_in[idx - 1][-2:] == "\r\n"
                    else len_stream - 1
                )
            if verbose:
                console.print(
                    f"line {line_no}: Computed /Length {len_stream} of obj {curr_obj}"
                )
            map_stream_len[curr_obj] = len_stream
        elif content == "endobj":
            curr_obj = None
        elif curr_obj is not None and len_stream is None:
            m_length_ref = RE_LENGTH_REF.match(line)
            if m_length_ref is not None:
                len_obj = m_length_ref.group(2)
                len_obj_gen = m_length_ref.group(3)
                if verbose:
                    console.print(
                        f"line {line_no}, /Length-reference {len_obj} {len_obj_gen} R: {content}"
                    )
                map_obj_length_ref[curr_obj] = len_obj
            else:
                m_length = RE_LENGTH.match(line)
                if m_length is not None:
                    if verbose:
                        console.print(f"line {line_no}, /Length: {content}")
                    map_obj_length_line[curr_obj] = line
                    map_obj_length_line_no[curr_obj] = line_no
        elif curr_obj is not None and len_stream is not None:
            len_stream += len(line.encode(encoding))
        elif line_xref is not None and line_no > line_xref + 2:
            objNo = line_no - line_xref - 2
            if objNo <= len(map_obj_offset) and str(objNo) in map_obj_offset:
                eol = line[-2:]
                xrefUpd = ("%010d" % map_obj_offset[str(objNo)]) + " 00000 n"
                if verbose:
                    console.print(f"{content} -> {xrefUpd}")
                line = xrefUpd + eol
        elif line_startxref is not None and line_no == line_startxref + 1:
            if offset_xref is None:
                raise NotImplementedError(
                    "Unsupported file: startxref without preceding xref-section (probable cross-reference stream)"
                )
            line = "%d\n" % offset_xref
        lines_out.append(line)

        offset_out += len(line.encode(encoding))

    # Some checks
    if len(map_obj_offset) == 0:
        raise RuntimeError(
            "Invalid PDF file: the command didn't find any PDF objects."
        )
    if offset_xref is None:
        raise RuntimeError(
            "Invalid PDF file: the command didn't find a xref-section"
        )
    if line_startxref is None:
        raise RuntimeError(
            "Invalid PDF file: the command didn't find a startxref-section"
        )

    for curr_obj, stream_len in map_stream_len.items():
        if curr_obj in map_obj_length_line:
            line = map_obj_length_line[curr_obj]
            m_length = RE_LENGTH.match(line)
            if m_length is None:
                raise RuntimeError(
                    f"Invalid PDF file: line '{line}' does not contain a valid /Length."
                )
            prev_length = m_length.group(2)
            len_digits = len(prev_length)
            len_format = "%%0%dd" % len_digits
            updated_length = len_format % stream_len
            if len(updated_length) > len_digits:
                raise RuntimeError(
                    f"Not enough digits in /Length-entry {prev_length}"
                    f" of object {curr_obj}:"
                    f" too short to take /Length {updated_length}"
                )
            line = m_length.group(1) + updated_length + m_length.group(3)
            lines_out[map_obj_length_line_no[curr_obj] - 1] = line
        elif curr_obj in map_obj_length_ref:
            len_obj = map_obj_length_ref[curr_obj]
            if len_obj not in map_obj_line:
                raise RuntimeError(
                    f"obj {curr_obj} has unknown length-obj {len_obj}"
                )
            len_obj_line = map_obj_line[len_obj]
            prev_length = lines_out[len_obj_line][:-1]
            len_digits = len(prev_length)
            len_format = "%%0%dd" % len_digits
            updated_length = len_format % stream_len
            if len(updated_length) > len_digits:
                raise RuntimeError(
                    f"Not enough digits in /Length-ref-entry {prev_length}"
                    f" of object {curr_obj} and len-object {len_obj}:"
                    f" too short to take /Length {updated_length}"
                )
            if prev_length != updated_length:
                if verbose:
                    console.print(
                        f"line {line_no}, ref-len {len_obj} of {curr_obj}: {prev_length} -> {updated_length}"
                    )
                lines_out[len_obj_line] = updated_length + "\n"
        else:
            raise RuntimeError(
                f"obj {curr_obj} with stream-len {stream_len} has no object-length-line: {map_obj_length_line}"
            )

    return lines_out


def read_binary_file(file_path: Path, encoding: str) -> list[str]:
    """
    Reads a binary file line by line and returns these lines as a list of strings in the given encoding.
    Encoding utf-8 can't be used to read random binary data.

    :param file_path: file to be read line by line
    :param encoding: encoding to be used (e.g. "iso-8859-1")
    :return lines including line-breaks
    """
    chunks: list[str] = []
    with file_path.open("rb") as file:
        buffer = bytearray()
        while True:
            chunk = file.read(4096)  # Read in chunks of 4096 bytes
            if not chunk:
                break  # End of file

            buffer += chunk

            # Split buffer into chunks based on LF, CR, or CRLF
            while True:
                match = re.search(b"(\x0d\x0a|\x0a|\x0d)", buffer)
                if not match:
                    break  # No more line breaks found, process the remaining buffer

                end = match.end()
                chunk_str = buffer[:end].decode(encoding, errors="strict")
                buffer = buffer[end:]

                chunks.append(chunk_str)

        # Handle the last chunk
        if buffer:
            chunks.append(buffer.decode(encoding, errors="strict"))

    return chunks


def main(file_in: Path, file_out: Path, encoding: str, verbose: bool) -> None:
    if not file_out:
        file_out = file_in
    console = Console()
    console.print(f"Read {file_in}")

    lines_in = read_binary_file(file_in, encoding)
    lines_out = update_lines(lines_in, encoding, console, verbose)

    with open(file_out, "wb") as f:
        for line in lines_out:
            f.write(line.encode(encoding))

    console.print(f"Wrote {file_out}", soft_wrap=True)
