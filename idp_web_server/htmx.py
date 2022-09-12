# Copyright 2019 Ingmar Dasseville, Pierre Carbonnelle
#
# This file is part of Interactive_Consultant.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os

from .HtmXgen import *
from .State import State


def wrap(static_file_dir, screen):
    """returns the `htmx.html` file with the unique `<div>` tag replaced by `screen` """

    path = os.path.join(static_file_dir, 'htmx.html')
    with open(path, mode='r', encoding='utf-8') as f:
        content = f.read()

    begin = content.find("<div")
    assert begin != -1, "begin marker not found !"
    end = content.find("</div>")
    assert end != -1, "end marker not found !"

    return content[:begin] + screen + content[end+len("</div>"):]


def file_openX(idp):
    state = State.make(idp, "{}", "{}", "[]")
    # ensure the stateful solvers are initialized
    _ = state.solver
    _ = state.optimize_solver
    _ = state.solver_reified
    _ = state.optimize_solver_reified

    tabs = dict()
    for decl in state.assignments.symbols.values():
        if decl.heading not in tabs:
            tabs[decl.heading] = decl.heading

    return render(
        div(cl="container", i=
            div(cl="row", i=
                div(cl="col s12 m6 push-m3", i=[
                    ul(cl="tabs", i=
                        [li(cl="tab col s3", i=
                            a(tab, href=f"#{hash(tab)}",
                                cl="active" if i==0 else None))
                        for i, tab in enumerate(tabs.values())])
                    , [ div(id=hash(tab), i=
                            ul(cl="collection", i=[
                                li(str(a.sentence), cl="collection-item")
                                for a in state.assignments.values()
                                if a.symbol_decl.heading == tab
                                ])
                            )
                        for tab in tabs.values()
                        ]
                    ])
                )
            )
        )