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
import urllib.parse

from idp_engine.Assignments import Status as S
from idp_engine.Expression import TRUE, FALSE
from idp_engine.utils import BOOL, INT, REAL, DATE

from .HtmXgen import *
from .State import State


def wrap(static_file_dir, screen):
    """returns the `htmx.html` file with the unique non-indented`<div>` tag replaced by `screen` """

    path = os.path.join(static_file_dir, 'htmx.html')
    with open(path, mode='r', encoding='utf-8') as f:
        content = f.read()

    begin = content.find("\n<div")
    assert begin != -1, "begin marker not found !"
    end = content.find("\n</div>")
    assert end != -1, "end marker not found !"

    return content[:begin] + screen + content[end+len("\n</div>"):]


def ass_head(ass):
    """generator for the head of an assignment"""
    if ass.sentence.type == BOOL:
        if ass.value and ass.value.same_as(TRUE):
            yield i("check", class_="material-icons")
        elif ass.value and ass.value.same_as(FALSE):
            yield i("clear", class_="material-icons")
    yield ass.sentence.code
    if ass.status not in [S.GIVEN, S.UNKNOWN, S.DEFAULT]:
        yield i("info", class_="material-icons")


def ass_body(ass):
    """generator for the body of an assignment"""
    if ass.status in [S.GIVEN, S.UNKNOWN, S.DEFAULT]:
        if ass.sentence.type == BOOL:
            yield   [label([
                        input(name=ass.sentence.code, type="checkbox", value="true",
                            checked=(ass.value and ass.value.same_as(TRUE)),
                            hx_trigger="click delay:50ms", hx_post="/htmx/state/post"),
                        span("yes", style="color: black;")
                    ]),
                    span("&nbsp;&nbsp;&nbsp;&nbsp;"),
                    label([
                        input(name=ass.sentence.code, type="checkbox", value="false",
                            checked=(ass.value and ass.value.same_as(FALSE)),
                            hx_trigger="click delay:50ms", hx_post="/htmx/state/post"),
                        span("no", style="color: black;")
                    ])]
        else:
            yield "TODO"
    else:
        yield "(consequence)"  # not shown


def stateX(state, update=False):
    """generator for the state"""

    tabs = dict()
    for decl in state.assignments.symbols.values():
        if decl.heading not in tabs:
            tabs[decl.heading] = decl.heading

    def tabsX():
        """ generates the content of the tabs """
        for index, tab in enumerate(tabs.values()):
            yield from div(id=f"tab-{index}", hx_swap_oob="innerHTML", i=
                            ul(class_="collapsible", i=[
                                li(i=[
                                    div(ass_head(ass),
                                        class_="collapsible-header")
                                    if ass.status in [S.GIVEN, S.UNKNOWN, S.DEFAULT] else
                                    div(ass_head(ass),
                                        class_="collapsible-header dont-unfold modal-trigger",
                                        href="#modal1", hx_trigger="click",
                                        hx_post="/htmx/state/explain?" +
                                            urllib.parse.urlencode(
                                                {ass.sentence.code: str(ass.value)},
                                                quote_via=urllib.parse.quote),
                                        hx_swap="none"),
                                    div(ass_body(ass), class_="collapsible-body")
                                    ])
                                for ass in state.assignments.values()
                                if ass.symbol_decl.heading == tab
                                and not ass.sentence.is_assignment()
                                ])
                            )

    if update:  # only send the content of the tabs
        return render(tabsX())
    else:  # generate the container
        return render(
            div(class_="container", id="container", i=
                div(class_="row", i=
                    form(i=
                        div(class_="col s12 m6 push-m3", i=[
                            ul(class_="tabs", i=
                                [li(class_="tab col s3", i=
                                    a(tab, id=f"#tab-{index}",
                                      href=f"#tab-{index}"))
                                for index, tab in enumerate(tabs.values())])
                            , tabsX()
                            ])
                        )
                    )
                )
        )

def explainX(facts, laws):
    return div(id="modal1", class_="modal", hx_swap_oob="innerHTML", i=[
               div(class_="modal_content", i=str(facts)),
               div(class_="modal_footer", i=
                   a("Close", href="#!",
                     class_="modal-close waves-effect waves-green btn-flat"))
    ])