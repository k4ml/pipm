#!/usr/bin/python

"""
ISC License

Copyright (c) 2019, Kamal Mustafa

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
"""

import os
import sys
import argparse

import subprocess
import functools

if hasattr(subprocess, 'run'):
    subprocess_run = subprocess.run
else:
    subprocess_run = subprocess.call

run_shell = functools.partial(subprocess_run, shell=True)

CWD = os.getcwd()
PYTHON = sys.executable
BASE_CMD = "PYTHONPATH=%s/local-packages %s -S" % (CWD, PYTHON)

def assert_python3():
    if sys.version_info.major < 3:
        print("Require python 3. You might want to change shebang to #!/usr/bin/python3")
        sys.exit(1)

def bootstrap():
    if os.path.exists('local-packages'):
        return

    # add setuptools and pip to local-packages so that we can
    # invoke python with -S flag going forward.
    run_shell("python -mpip install -t local-packages setuptools pip")

def main(args=sys.argv[1:]):
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='PROG')
    parser.add_argument('command', help='command to run')
    parsed_args, rest = parser.parse_known_args(args)
    if parsed_args.command == 'run':
        run_parser = argparse.ArgumentParser(prog='pipm run')
        run_parser.add_argument('module', help='module to run')
        run_args, run_rest = run_parser.parse_known_args(rest)
        module = run_args.module
        rest = run_rest
    else:
        if parsed_args.command == 'install':
            module = 'pip %s -t local-packages' % parsed_args.command
        else:
            module = 'pip %s' % parsed_args.command

    command_args = ["'%s'" % arg for arg in rest]

    if module == 'python':
        commands = BASE_CMD + " " + " ".join(command_args)
    else:
        commands = BASE_CMD + " -m%s" % module + " " + " ".join(command_args)

    run_shell(commands)

if __name__ == "__main__":
    main()
