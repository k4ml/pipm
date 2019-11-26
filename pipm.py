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
BASE_CMD = "PYTHONPATH=%s/local-packages %s -S -mpip" % (CWD, PYTHON)
RUN_CMD = "PYTHONPATH=%s/local-packages %s -S" % (CWD, PYTHON)

def install(args):
    run_shell(BASE_CMD + " install -t local-packages " + " ".join(args.packages))

def run(args):
    if args.command != 'python':
        command = ' -m%s ' % args.command
    else:
        command = ""

    command_args = ["'%s'" % arg for arg in getattr(args, 'command-args')]
    command = RUN_CMD + command + " " + " ".join(command_args)
    run_shell(command)

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
    parser.add_argument('--foo', action='store_true', help='foo help')
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_install = subparsers.add_parser('install', help='a help')
    parser_install.add_argument('packages', type=str, help='Package name to install', nargs="+")
    parser_install.set_defaults(func=install)

    parser_run = subparsers.add_parser('run', help='b help')
    parser_run.add_argument('command', type=str, help='command to run')
    parser_run.add_argument('command-args', type=str, help='arguments for command', nargs="*")
    parser_run.set_defaults(func=run)

    assert_python3()
    bootstrap()
    parsed_args = parser.parse_args(args)
    parsed_args.func(parsed_args)

if __name__ == "__main__":
    main()
