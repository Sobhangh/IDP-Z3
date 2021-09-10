# Copyright 2019 Ingmar Dasseville, Pierre Carbonnelle

# This file is part of Interactive_Consultant.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""

The command-line program to execute an IDP file with a main() block.

"""

import argparse
import os
import sys

from idp_engine import IDP
from contextlib import redirect_stdout


def cli(args=None):
    parser = argparse.ArgumentParser(description='IDP-Z3')
    parser.add_argument('FILE', help='path to the .idp file', type=str)
    parser.add_argument('-o', '--output', help='name of the output file',
                        type=str)
    args = parser.parse_args()

    error = 0
    if args.FILE:
        dir = os.getcwd()
        file = os.path.join(dir, args.FILE)
        with open(file, "r") as f:
            theory = f.read()

        idp = IDP.from_str(theory)
        if not args.output:
            # Print output to stdout.
            idp.execute()
        else:
            # Print output to file.
            with open(args.output, mode='w', encoding='utf-8') \
                    as buf, redirect_stdout(buf):
                try:
                    idp.execute()
                except Exception as exc:
                    print(exc)

    else:
        parser.print_help()

    sys.exit(error)


if __name__ == "__main__":
    cli()
