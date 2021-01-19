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
import time

from idp_solver import idpparser


def run_idp(idp):
    start = time.time()
    idp = idpparser.model_from_str(idp)
    idp.execute()
    return time.time() - start


def cli(args=None):
    parser = argparse.ArgumentParser(description='IDP-Z3')
    parser.add_argument('inputfile', type=str,
                        help='path to the input file')
    parser.add_argument('--outputfile', '-o', type=str,
                        help='path to the output file')
    args = parser.parse_args()
    error = 0

    inputf = os.path.abspath(args.inputfile)
    with open(inputf, "r") as f:
        idp = f.read()

    time = 0
    if not args.outputfile:
        time = run_idp(idp)
    else:
        with open(args.outputfile, "w") as out:
            from io import StringIO
            old = sys.stdout
            sys.stdout = stdout = StringIO()
            sys.stdout = stdout

            time = run_idp(idp)

            sys.stdout = old
            out.write(str(stdout.getvalue()))

    print("Elapsed time: {} seconds".format(time))
    sys.exit(error)


if __name__ == "__main__":
    cli()
