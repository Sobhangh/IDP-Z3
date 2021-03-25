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


def cli(args=None):
    parser = argparse.ArgumentParser(description='IDP-Z3')
    parser.add_argument('FILE', nargs='*')
    args = parser.parse_args()

    error = 0
    if args.FILE:
        dir = os.path.dirname(__file__)
        file = os.path.join(dir, args.FILE[0])
        with open(file, "r") as f:
            theory = f.read()

        idp = IDP.parse(theory)
        idp.execute()

    sys.exit(error)


if __name__ == "__main__":
    cli()
