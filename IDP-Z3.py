"""
    Copyright 2019 Ingmar Dasseville, Pierre Carbonnelle

    This file is part of Interactive_Consultant.

    Interactive_Consultant is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Interactive_Consultant is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with Interactive_Consultant.  If not, see <https://www.gnu.org/licenses/>.
"""

"""

The program to execute an IDP file with a main() block.

"""

import argparse
import os
import sys

from Idp import idpparser


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='IDP-Z3')
    parser.add_argument('FILE', nargs='*')
    args = parser.parse_args()

    error = 0
    if args.FILE:
        dir = os.path.dirname(__file__)
        file = os.path.join(dir, args.FILE[0])
        with open(file, "r") as f:
            theory = f.read()
        
        idp = idpparser.model_from_str(theory)
        idp.execute()

    sys.exit(error)