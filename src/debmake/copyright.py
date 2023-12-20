#!/usr/bin/python3
# vim:se tw=0 sts=4 ts=4 et ai:
"""
Copyright © 2014 Osamu Aoki

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import glob
import os
import sys

###################################################################
# Format licence
###################################################################
def format_license(lines):
    # RFC-822 compliant empty lines with "."
    xlines = []
    for line in lines:
        line = line.rstrip()
        if line == "":
            xlines.append(" .\n")
        else:
            xlines.append(" " + line + "\n")
    return "".join(xlines)


#######################################################################
# license text file conversion
#######################################################################
def license_text(file, encoding="utf-8"):
    lines = []
    try:
        with open(file, "r", encoding=encoding) as fd:
            for line in fd.readlines():
                lines.append(line.rstrip())
    except UnicodeDecodeError as e:
        print(
            "W: Non-UTF-8 char found, using latin-1: {}".format(file), file=sys.stderr
        )
        fd.close()
        lines = []
        with open(file, "r", encoding="latin-1") as fd:
            for line in fd.readlines():
                lines.append(line.rstrip())
    return format_license(lines)


#######################################################################
# main program
#######################################################################
def copyright(
    package_name,
    license_file_masks,
    cdata,
    xml_html_files,
    binary_files,
    huge_files,
    mode=0,
    tutorial=False,
):
    # mode: 0: not -c, 1: -c simple, 2: -cc normal, 3: -ccc extensive
    #      -1: -cccc debug simple, -2 -ccccc debug normal -3 -cccccc debug extensive
    # make text to print
    text = """\
Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: {}
Upstream-Contact: <preferred name and address to reach the upstream project>
Source: <url://example.com>
""".format(
        package_name
    )
    if tutorial:
        text += """###
### Uncomment the following 2 lines to enable uscan to exclude non-DFSG components
### Files-Excluded: command/non-dfsg.exe
###   docs/source/javascripts/jquery-1.7.1.min.js
###
### This is a autogenerated template for debian/copyright.
###
### Edit this according to the "Machine-readable debian/copyright file" as
### http://www.debian.org/doc/packaging-manuals/copyright-format/1.0/ .
###
### Generate updated license templates with the "debmake -cc" to STDOUT
### and merge them into debian/copyright as needed.
###
### Please avoid to pick license terms that are more restrictive than the
### packaged work, as it may make Debian's contributions unacceptable upstream.
#
# Please double check copyright with the licensecheck(1) command.

"""
    else:
        text += (
            "#\n# Please double check copyright with the licensecheck(1) command.\n\n"
        )
    for (licenseid, licensetext, files, copyright_lines) in cdata:
        # Files:
        text += "Files:     {}\n".format("\n           ".join(files))
        # Copyright:
        text += "Copyright: " + copyright_lines[11:]
        # License:
        text += "License:   {}{}\n\n".format(licenseid, licensetext)
    if xml_html_files != []:
        text += "#----------------------------------------------------------------------------\n"
        text += "# xml and html files (skipped):\n#         {}\n\n".format(
            "\n#         ".join(xml_html_files)
        )
    if binary_files != []:
        text += "#----------------------------------------------------------------------------\n"
        text += "# binary files (skipped):\n#         {}\n\n".format(
            "\n#         ".join(binary_files)
        )
    if huge_files != []:
        text += "#----------------------------------------------------------------------------\n"
        text += "# huge files   (skipped):\n#         {}\n\n".format(
            "\n#         ".join(huge_files)
        )
    if mode == 0:  # not for -c
        text += """\
#----------------------------------------------------------------------------
# Files marked as NO_LICENSE_TEXT_FOUND may be covered by the following
# license/copyright files.

"""
        # get list of files to attach
        license_files = set()
        for fx in license_file_masks:
            license_files.update(set(glob.glob(fx)))
        for f in license_files:
            if os.path.isfile(f):  # if only a real file
                text += "#----------------------------------------------------------------------------\n"
                text += "# License file: {}\n".format(f)
                text += license_text(f)
                text += "\n"
    return text


#######################################################################
# Test script
#######################################################################
if __name__ == "__main__":
    # licenseid, licensetext, files, copyright_lines
    print(
        copyright(
            "foo",
            {"LICENSE*", "COPYRIGHT"},
            [
                (
                    "LICENSE_ID",
                    """
 LICENSE-1
 LICENSE-2
 .
 LICENSE-3
 LICENSE-4""",
                    ["file1", "file2"],
                    """           COPYRIGHT-1
           COPYRIGHT-2
           COPYRIGHT-3
           COPYRIGHT-4
           COPYRIGHT-5
""",
                )
            ],
            ["xml1.file", "xml2.file"],
            ["binary1.file", "binary2.file"],
            ["huge.file1", "huge.file2"],
        )
    )
