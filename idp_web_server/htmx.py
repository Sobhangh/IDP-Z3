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

from htmx_gen import *
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


def ass_head(ass, id=None):
    """generator for the head of an assignment"""
    def info():
        if ass.status not in [S.GIVEN, S.UNKNOWN, S.DEFAULT]:
             yield i("info", class_="material-icons")

    if ass.sentence.type == BOOL:
        yield span([
            i("check" if ass.value.same_as(TRUE) else "clear",
              class_="material-icons") if ass.value is not None else "",
            ass.sentence.code,
            info()
        ])
    elif (0 < len(ass.symbol_decl.range)
        and ass.status in [S.GIVEN, S.UNKNOWN, S.DEFAULT]):  # get possible values
        yield span(hx_trigger="click", hx_swap="none",
                   hx_post="/htmx/state/values?"+urllib.parse.urlencode({ass.sentence.code: id}),
                   i=[ass.sentence.code,
                      f" = {ass.value}" if ass.value else "",
                      info() ])
    elif ass.sentence.type in [INT, REAL]:
        yield span([
            ass.sentence.code,
            f" = {float(ass.value.py_value)}" if ass.value else "",
            info()
        ])
    else:
        yield span([
            ass.sentence.code,
            f" = {ass.value}" if ass.value else "",
            info()
        ])


def ass_body(ass, state):
    """generator for the body of an assignment"""
    if ass.sentence.type == BOOL:
        if ass.status in [S.GIVEN, S.UNKNOWN, S.DEFAULT]:
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
            yield ""
    elif 0 < len(ass.symbol_decl.range):
        yield div([input(name=ass.sentence.code, type="hidden",
                            value=ass.value)
                   if ass.status in [S.GIVEN, S.DEFAULT] else "",
                    [input(name=a.sentence.code, type="hidden", value="false")
                    for a in state.assignments.values()
                    if a.status in [S.GIVEN, S.DEFAULT] and a.value.same_as(FALSE)
                    and a.sentence.code.startswith(ass.sentence.code + " = ")]
        ])
    elif ass.sentence.type in [INT, REAL]:
        if ass.status in [S.GIVEN, S.UNKNOWN, S.DEFAULT]:
            yield input(name=ass.sentence.code, type="number",
                        value=str(float(ass.value.py_value)) if ass.value else None,
                        hx_trigger="change", hx_post="/htmx/state/post")
        else:
            yield ""
    else:
        yield "TODO"  # not shown


def stateX(state, update=False):
    """generator of the tabs representing the state"""

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
                                    div(ass_head(ass, f"tab-{index}-{index2}"),
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
                                    div(ass_body(ass, state), class_="collapsible-body teal lighten-5",
                                        id=f"tab-{index}-{index2}",)
                                    ])
                                for index2, ass in enumerate(state.assignments.values())
                                if ass.symbol_decl.heading == tab
                                and not ass.sentence.is_assignment()
                                and not ass.status == S.UNIVERSAL
                                ])
                            )

    if update:  # only send the content of the tabs
        return render(tabsX())
    else:  # generate the container
        return render(
            div(class_="container", id="container", i=
                div(class_="row", i=
                    form(div(class_="col s12 m6 push-m3", i=[
                            div(class_="progress htmx-indicator", i=div(class_="indeterminate")),
                            ul(class_="tabs", i=
                                [li(class_="tab col s3", i=
                                    a(tab, id=f"#tab-{index}",
                                      href=f"#tab-{index}"))
                                for index, tab in enumerate(tabs.values())])
                            , tabsX()
                            ]),
                        hx_indicator=".progress"
                        )
                    )
                )
        )


def ass_explain(ass, hidden=False):
    """generator for the body of an assignment for explanation"""
    if ass.sentence.type == BOOL:
        yield   label( style="display: none" if hidden else None, i=[
                    input(name=ass.sentence.code, type="checkbox",
                          value="true" if ass.value.same_as(TRUE) else "false",
                          checked="true", class_="modal-close",
                          hx_trigger="click", hx_post="/htmx/state/post"),
                    span(("" if ass.value.same_as(TRUE) else "Not ")+ass.sentence.code,
                         style="color: black;")
                ])
    elif 0 < len(ass.symbol_decl.range):
        yield   label( style="display: none" if hidden else None, i=[
                    input(name=ass.sentence.code, type="checkbox",
                          value=ass.value.code,
                          checked="true", class_="modal-close",
                          hx_trigger="click", hx_post="/htmx/state/post"),
                    span(f"{ass.sentence.code} = {ass.value}",
                         style="color: black;")
                ])
    elif ass.sentence.type in [INT, REAL]:
        yield   label( style="display: none" if hidden else None, i=[
                    input(name=ass.sentence.code, type="checkbox",
                          value=str(float(ass.value.py_value)),
                          checked="true", class_="modal-close",
                          hx_trigger="click", hx_post="/htmx/state/post"),
                    span(f"{ass.sentence.code} = {ass.value}",
                         style="color: black;")
                ])
    else:
        yield "TODO " + ass.sentence.code + (" : hidden" if hidden else "False")


def valuesX(state, sentence, values, index):
    """ generates the entry form for a term with an enumerated type """

    def d(inner, align="center"):
        """ generates a custom td """
        yield from td(inner,
                      style=f"padding: 5px 5px; text-align: left; valign: top")

    def ass(sentence, v):
        """ returns the assignment `sentence = v` in state.assignments, if any """
        return state.assignments.get(f"{sentence} = {v.code}", None)

    def ass_is_false(sentence, v):
        """ True if state.assignments[sentence = v] is false """
        return (ass(sentence, v) is not None
                and ass(sentence,v).value is not None
                and ass(sentence, v).value.same_as(FALSE))

    return div(id=index, hx_swap_oob="innerHTML", i=[
        table(class_="highlight", i=[
            tr([d('Yes'), d(""), d("No")]),
            [tr(style="border-bottom: 0px", i=[
                d(label([input(name=f"{sentence} = {v.code}", type="checkbox", value="true",
                               checked=(str(state.assignments[sentence].value) == v.code),
                               hx_trigger="click delay:50ms", hx_post="/htmx/state/post"),
                          span("", style="valign: top")])
                  if not ass_is_false(sentence,v) else ""),
                d(v.code, "left"),
                d(label([input(name=f"{sentence} = {v.code}", type="checkbox", value="false",
                               checked=ass_is_false(sentence, v),
                               disabled="true" if (ass_is_false(sentence, v)
                                        and ass(sentence, v).status != S.GIVEN) else
                                        None,
                               hx_trigger="click delay:50ms", hx_post="/htmx/state/post"),
                         span("", style="valign: top")]))])
             for v in state.assignments[sentence].sentence.decl.range]])
        ])


def explainX(state, facts, laws):
    """ generator for the modal """
    return div(id="modal1", class_="modal", hx_swap_oob="innerHTML", i=[
               div(class_="modal_content container", i=
                   form([
                     p("This is a consequence of the following choices (which you can undo):"),
                     [div([ass_explain(ass)]) for ass in facts],  # explaining facts
                     [ass_explain(ass, hidden=True) for ass in state.assignments.values()
                      if all(ass.sentence.code not in f.sentence.code for f in facts)
                      and ass.status in [S.GIVEN, S.DEFAULT]],  # other facts
                     p("Applicable laws:"),
                     [p("* "+law.annotations['reading']) for law in laws]])),
                div(class_="modal_footer", i=
                   a("Close", style="color: teal",
                     class_="modal-close waves-effect waves-green btn-flat")),
                span(i("clear", class_="material-icons", style="color: teal"),
                     class_="modal-close", style="position: absolute; right: 0; top: 0")
    ])