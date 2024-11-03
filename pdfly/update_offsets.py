#!/usr/bin/env python
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
Therefore it expects that there a no binary streams.
It expects that there is one xref-section only.
It expects that the /Length-entries have default values containing
enough digits, e.g. /Length 000 when the stream consists of 576 bytes.

EXAMPLE
   update-offsets -v --encoding UTF-8 issue-297.pdf issue-297.out.pdf
"""

from collections.abc import Iterable
from pathlib import Path
from rich.console import Console
import re
import sys


def update_lines(lines_in: Iterable[str], encoding: str, console: Console, verbose: bool) -> Iterable[str]:
    """Iterates over the lines of a pdf-files and updates offsets.

    The input is expected to be a pdf without binary-sections.

    :param lines_in: An Iterable over the lines including line-breaks.
    :param encoding: The encoding, e.g. "iso-8859-1" or "UTF-8".
    :param console: Console used to print messages.
    :param verbose: True to activate logging of info-messages.
    :return The output is a list of lines to be written
            in the given encoding.
    """
    re_obj = re.compile(r"^([0-9]+) ([0-9]+) obj *")
    re_content = re.compile(r"^(.*)")
    re_length = re.compile(r"^(.*/Length )([0-9]+)( .*)", re.DOTALL)

    lines_out = []  # lines to be written
    map_line_offset = {}  # map from line-number to offset
    map_obj_offset = {}  # map from object-number to offset
    line_no = 0  # current line-number (starting at 0)
    offset_out = 0  # current offset in output-file
    line_xref = None  # line-number of xref-line (in xref-section only)
    line_startxref = None  # line-number of startxref-line
    curr_obj = None  # number of current object
    len_stream = None  # length of stream (in stream only)
    offset_xref = None  # offset of xref-section
    map_stream_len = {}  # map from object-number to /Length of stream
    map_obj_length_line = {}  # map from object-number to /Length-line
    map_obj_length_line_no = {}  # map from object-number to line_no
    # of /Length-line
    for line in lines_in:
        line_no += 1
        m_content = re_content.match(line)
        if m_content is None:
            raise RuntimeError(f"Line {line_no} without line-break.")
        content = m_content.group(1)
        map_line_offset[line_no] = offset_out
        m_obj = re_obj.match(line)
        if m_obj is not None:
            curr_obj = m_obj.group(1)
            if verbose:
                console.print(f"line {line_no}: object {curr_obj}")
            map_obj_offset[curr_obj] = int(offset_out)
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
                    f"Line {line_no}: " + "endstream without object-start."
                )
            if len_stream is None:
                raise RuntimeError(f"Line {line_no}: endstream without stream.")
            if verbose:
                console.print(f"line {line_no}: /Length {len_stream}")
            map_stream_len[curr_obj] = len_stream
        elif content == "endobj":
            curr_obj = None
        elif curr_obj is not None and len_stream is None:
            mLength = re_length.match(line)
            if mLength is not None:
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
                raise RuntimeError("startxref without preceding xref-section")
            line = "%d\n" % offset_xref
        lines_out.append(line)

        offset_out += len(line.encode(encoding))

    # Some checks
    if len(map_obj_offset) == 0:
        raise RuntimeError("The command didn't find any PDF objects.")
    if offset_xref is None:
        raise RuntimeError("The command didn't find a xref-section")
    if line_startxref is None:
        raise RuntimeError("The command didn't find a startxref-section")

    for curr_obj, stream_len in map_stream_len.items():
        if not curr_obj in map_obj_length_line:
            raise RuntimeError(
                f"obj {curr_obj} with stream-len {len}"
                + f" has no object-length-line: {map_obj_length_line}"
            )
        m_length = re_length.match(map_obj_length_line[curr_obj])
        prev_length = m_length.group(2)
        len_digits = len(prev_length)
        len_format = "%%0%dd" % len_digits
        updated_length = len_format % stream_len
        if len(updated_length) > len_digits:
            raise RuntimeError(
                f"Not enough digits in /Length-entry {m_length.group(2)}"
                + f" of object {curr_obj}:"
                + f" too short to take /Length {updated_length}"
            )
        line = m_length.group(1) + updated_length + m_length.group(3)
        lines_out[map_obj_length_line_no[curr_obj] - 1] = line

    return lines_out


def main(file_in: Path, file_out: Path, encoding: str, verbose: bool) -> None:
    console = Console()
    console.print(f"Read {file_in}")

    with open(file_in, "r") as f:
        lines_out = update_lines(f, encoding, console, verbose)

    with open(file_out, "wb") as f:
        for line in lines_out:
            f.write(line.encode(encoding))

    console.print(f"Wrote {file_out}")
