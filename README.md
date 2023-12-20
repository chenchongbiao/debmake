# Debmake

This is the new debmake program written in Python.  This provides convenient
command to make a Debian package from the upstream VCS/tarball/source-tree.

This is available as the "debmake" package on Debian.

 * Homepage: https://salsa.debian.org/debian/debmake
 * Default branch: main

See the HTML files in the "debmake-doc" package for the introductory guide.

## License for the entire source

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### FILES outside of extra/

  * Copyright © 2013-2021 Osamu Aoki <osamu@debian.org>

### FILES in extra/
  * Copyright © Jim Van Zandt <jrv@debian.org>
  * Copyright © Santiago Vila <sanvila@ctv.es>
  * Copyright © Dirk Eddelbuettel <edd@debian.org>
  * Copyright © Nils Naumann <naumann@unileoben.ac.at>
  * Copyright © Jim Van Zandt <jrv@debian.org>
  * Copyright © 2013 Osamu Aoki <osamu@debian.org>

These are originally generated by the output of the dh_make command.  The
output has been edited by Osamu Aoki to fit into this package.  The dh-make
package came with the GPL license with the following permissive exception:

  As a special exception, when the template files are copied by dh-make into
  dh-make output files, you may use those output files without restriction.
  This special exception was added by Craig Small in version 0.37 of dh-make.

Since this exception is permissive, I am releasing the entire source package
under permissive MIT license as above.

### History

The author thanks previous efforts on this topic (GPL):
 * debmake: command: deb-make, version up to 3.8         (shell script)
   * 1996-1997 Christoph Lameter <clameter@debian.org>
   * 1997-2006 Santiago Vila <sanvila@debian.org>
 * dh-make: command: dh_make                             (perl script)
   * 1998-2012 Craig Small <csmall@debian.org>
     (This is active project in 2021.  Around 2016, dh-make was ported to
      python code base with major updates.)

## How to install

Debian/Ubuntu package to a system:

    $ sudo apt-get install debmake

For other POSIX system, you can create a wheel package and install it with pip
or pipx.  For example with pipx into venv.

    $ python3 setup.py bdist_wheel
    $ pipx install dist/debmake*.wheel

($PATH should be set to include ~/.local/bin )

## How to modify as contributor

1. Check-out default branch "main":
        $ git clone https://salsa.debian.org/debian/debmake.git
2. Make modification to "main" branch (or your private topic branch
   and send us your pull request or patch).

## How to update as upstream before release

1. Update `src/debmake/__init__.py` with new upstream version `4.1.2`
2. Add a new entry to the debian/changelog with the new upstream version
   ("`dch -i`" creates entry such as `4.1.1-2` --> change to `4.1.2-1`)
3. When debmake command line interface changes:
      * update debmake-doc package
      * generate a new `debmake.1` file in its source
      * copy generated `debmake.1` file into `manpages/debmake.1`
4. Update `test/.LICENSE.KEEP` if test results changes by the following:
```
        $ cd test/src; make
          ... verify it is SUCCESS
```
  (If new test case is added and it build result is good, copy the new
   `test/.LICENSE.LOG` to `test/.LICENSE.KEEP` to make
   this SUCCESS)
5. Tag it with upstream version `4.1.2` and build with
```
        $ git tag -s 4.1.2
        $ git deborig
	$ sbuild
```
6. Clean source tree with
```
        $ git clean -d -f -x
```

7. Make source only upload.
```
        $ dgit push-source
```

(Initial dgit transition needs more work with `--deliberately-not-fast-forward`
or `--overwrite`.  See dgit-maint-merge(7))

Please follow PEP-8 as much as possible.
 * format source with "black"
 * indent 4 spaces
 * 80 char/line
 * Coding style exceptions:
   * line for debug code -> single line for ease of "grep"
   * some regex (max 100 char/line) for readability

## Debug the source code without installing it as deb package

There are 2 debugging purpose executable files for the Debian package:
 * `/usr/lib/debmake/debmake-lc`
 * `/usr/lib/debmake/debmake-dep5`

These are not meant to be general use and has no manpage so they are moved out
of /usr/bin for Debian package.  These can help check situation inside debmake
for debug purpose.

The source code can be tested by installing its wheel package to your user
environment.

```
 $ python3 setup.py bdist_wheel
 $ pipx install dist/debmake*.whl
```
Here, I use pipx to install debmake module into venv and let it set symlinks in
~/.local/bin` to executable files for debugging.  Now all scripts such as
`debmake` providing `debmake` equivalent command, `debmake-lc` providing
`/usr/lib/debmake/debmake-lc` command equivalent, `debmake-dep5` providing
`/usr/lib/debmake/debmake-dep5` command equivalent can be executed
independently from the command line for debugging.

 * ```debmake [-h] [-c | -k] [-n | -a package-version.tar.gz | -d | -t]```
```
               [-p package] [-u version] [-r revision] [-z extension]
               [-b binarypackage[:type]] [-e foo@example.org]
               [-f "firstname lastname"] [-i [debuild|pdebuild|...] | -j]
               [-l "license_file"] [-m] [-o "file"] [-q] [-s] [-v] [-w args]
               [-x [01234]] [-y] [-L] [-P] [-T]
```
 * ```debmake-dep5.py [-s|-c|-t|-i|--] <file>```
```
        -s  selftest
        -c  extract copyright info as formatted text
        -t  extract license info as plain text
        -i  check license ID with extra info
        --  check license ID and extract copyright (default)
```
 * ```debmake-lc.py [-][1|2|3|4|5|6] <files ...>```

```
   check <files ...> for license ID in different mode of -c options in debmake
        1: -c        license ID
        2: -cc       license ID + license text
        3: -ccc      license ID + license text + extra
        -1: -cccc    license ID + internal ID
        -2: -ccccc   license ID + internal ID + license text
        -4: -cccccc  license ID + internal ID + license text + extra
        5: sub-string match for debug
        6: combination sub-string match for debug
```

There are ways to test these code in place without installing them.  One way is
to set up the module loading path `$PYTHONPATH` to `src/`; and the command
search path `$PATH` to be extended to include `src/debmake/` respectively from
where `setup.py` is found by sourcing as:
```
          $ source setenv
```

Now all scripts are available to the shell as:
 * `__main__.py` providing `/usr/bin/debmake` equivalent
 * `lc.py` providing `/usr/lib/debmake/debmake-lc` equivalent
 * `checkdep5.py` providing `/usr/lib/debmake/debmake-dep5` equivalent

An alternative approach to start debamke's `main()` in place is:

```
 $ cd src
 $ python3 -m debmake
```

The last one doesn't need to set up environment variables `$PATH` and
`$PYTHONPATH` but your working directory must be at `src/`.

Since setting proper environment variables `$PATH` and `$PYTHONPATH` or
executing a command from a particular path are confusing, I don't recommend
testing code in place.

Trouble shoot hints:
 * What to do for strange string contaminating license info?
   *  => Fix `check_lines()`       in src/debmake/checkdep5.py
 * What to do for incorrect range calculation for copyright years.
   *  => Fix `analyze_copyright()` in src/debmake/checkdep5.py
 * What to do for strange license type assignment?
   * => Fix `lc()`                in src/debmake/lc.py

## Hints for reading the source

How copyright files are scanned by debmake in normal usage?

```
    -k option execution  --> debmake/kludge.py    kludge()
    -c option execution  +-> debmake/scanfiles.py scanfiles()
                         +-> debmake/checkdep5.py checkdep5()
    normal execution     --> debmake/debian.py    debian()
                         +-> debmake/copyright.py copyright()
                                 Here, copyformat() gets:
                                   para['package']
                                   para['license']
                                   para['cdata']
                                   para['xml_html_files']
                                   para['binary_files']
                                   para['huge_files']
               These are set by debmake/analyze.py analyze(para) calling:
                                   -+--> debmake/scanfiles.py scanfiles()
                                    +--> debmake/checkdep5.py checkdep5()
```

(PATH are relative to `src/`)

What does `scanfiles()` do?
  * Scan all files in source tree and make list of files for each category:
    * nonlink_files, xml_html_files, binary_files, huge_files
  * extensions holds all file extension types

What does `checkdep5()` do?
  * Scan nonlink_files and return summary of copyright info as cdata
  by 3 step operations:
```
        adata = check_all_licenses()
        bdata = bunch_all_licenses(adata)
        cdata = format_all_licenses(bdata)
              = [(licenseid, licensetext, files, copyright_lines), ...]
```
What does `check_all_licenses()` do?
```
    for each file:
      (copyright_data, license_lines) = checkdep5(file, ...)
        This extract copyright iand license information section
        out of file using check_lines()
      norm_text = debmake.lc.normalize(license_lines)
        This normalize copyright info.
      (licenseid, licensetext, permissive) = debmake.lc.lc(norm_text, ...)
        This characterize license info from norm_text
        Here, md5hashkey is used to optimize operation speed
```
Osamu Aoki, Wed, 08 Aug 2018 13:01:57 +0000
 -- Updated June 2021
