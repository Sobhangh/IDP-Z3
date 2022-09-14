# Copyright 2019 Pierre Carbonnelle
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

"""
This module contains functions to generate HTML conveniently and efficiently.

It is an alternative to templating engines, like Jinja,
e.g., for use with [htmx](https://htmx.org/).

Pros:
* use familiar python syntax
* use efficient concatenation techniques
* optional indentation

Cons:
* the name of some tag attributes is changed
(e.g., `class_` instead of `class`, due to Python parser)


Tutorial:
---------

A tag is created by calling a function of the appropriate name:

>>> print(render(p("text")))
<p>text</p>


Tag attributes are specified using named arguments:

>>> print(render(br(id="1")))
<br id="1">

>>> print(render(br(id=None)))
<br>

>>> print(render(ul(li("text", selected=True))))
<ul><li selected>text</li></ul>

>>> print(render(ul(li("text", selected=False))))
<ul><li>text</li></ul>


Some tag attributes are changed: you must use `class_` instead of `class`,
`for_` instead of `for`, and `_` instead of `-`.

>>> print(render(p("text", class_="s12", hx_get="url")))
<p class="s12" hx-get="url">text</p>

>>> print(render(button("Click me", hx_post="/clicked", hx_swap="outerHTML")))
<button hx-post="/clicked" hx-swap="outerHTML">Click me</button>


The innerHTML can be a list:

>>> print(render(div(["text", span("item 1"), span("item 2")])))
<div>text<span>item 1</span><span>item 2</span></div>

The innerHTML can also be a list of lists:

>>> print(render(div(["text", [span(f"item {i}") for i in [1,2]]])))
<div>text<span>item 1</span><span>item 2</span></div>


The innerHTML can also be specified using the `i` parameter,
after the other attributes, to match the order of rendering:

>>> print(render(ul(class_="s12", i=[li("item 1"), li("item 2")])))
<ul class="s12"><li>item 1</li><li>item 2</li></ul>


For debugging your code, you can set global variable `indent` to `True`
in the code below (or call `indent_it(True)`)
to obtain HTML with tag indentation, e.g.,

>>> indent_it(True); print(render(div(class_="s12", i=["text", span("item 1"), span("item 2")])))
<div class="s12">
  text
  <span>
    item 1
  </span>
  <span>
    item 2
  </span>
</div>
<BLANKLINE>

"""

indent = False


from typing import Iterator, List, Optional, Union

Tag = Iterator[str]

_tab = "  "
_cr = "\n"

def indent_it(value):
    global indent
    indent = value

def render(gen: Tag) -> str:
    return ''.join(gen)


def solo_tag(tag_name: str, ** kwargs) -> Tag:
    """returns a tag without body, e.g. `<br id="1">`

    Args:
        tag_name : name of the tag
        kwargs (Dict[str, Optional[Union[str, bool]]]): attributes of the tag
            The `i` attributes, if present, is actually the innerHtml of the tag

    Yields:
        Tag: a string iterator to be rendered
    """

    kwargs = { k.replace("class_", "class").replace("for_", "for").replace("_", "-"): v
               for k, v in kwargs.items()
               if v is not None and (type(v) != bool or v)}

    attrs = ""
    for k,v in kwargs.items():
        if type(v) == bool:
                attrs += f' {k}'
        else:
                attrs += f' {k}="{v}"'

    yield f"<{tag_name}{attrs}>{_cr if indent else ''}"


def tag(tag_name: str,
        body: Optional[Union[str, Tag, List[Union[str, Tag, List[Tag]]]]] = None,
        **kwargs
        ) -> Tag:
    """returns a generator of strings, to be rendered as a HTML tag of type `name`

    Args:
        tag_name : name of the tag
        body : body of the tag, or None
        kwargs (Dict[str, Optional[Union[str, bool]]]): attributes of the tag
            The `i` attributes, if present, is actually the innerHtml of the tag

    Yields:
        Tag: a string iterator to be rendered
    """
    if 'i' in kwargs:
        body = kwargs['i']
        del kwargs['i']

    yield from solo_tag(tag_name, **kwargs)

    if body is not None:
        if type(body) == str:  # body is a str
            yield (f"{_tab}{body}{_cr}" if indent else body)
        else:
            for b in body:
                if type(b) == str:  # body is a Tag
                    yield (f"{_tab}{b}{_cr}" if indent else b)
                else:
                    for b1 in b:
                        if type(b1) == str:  # body is a List[Tag]
                            yield (f"{_tab}{b1}" if indent else b1)
                        else:
                            for b2 in b1:  # body is a List[List[Tag]]
                                yield (f"{_tab}{b2}" if indent else b2)

    yield f"</{tag_name}>{_cr if indent else ''}"


# in alphabetic order

def a(body=None, **kwargs):
    yield from tag("a", body, **kwargs)


def br(**kwargs):
    yield from solo_tag("br", **kwargs)

def button(body=None, **kwargs):
    yield from tag("button", body, **kwargs)


def div(body=None, **kwargs):
    yield from tag("div", body, **kwargs)


def form(body=None, **kwargs):
    yield from tag("form", body, **kwargs)


def i(body=None, **kwargs):
    yield from tag("i", body, **kwargs)


def input(**kwargs):
    yield from solo_tag("input", **kwargs)


def label(body=None, **kwargs):
    yield from tag("label", body, **kwargs)


def li(body=None, **kwargs):
    yield from tag("li", body, **kwargs)


def p(body=None, **kwargs):
    yield from tag("p", body, **kwargs)


def span(body=None, **kwargs):
    yield from tag("span", body, **kwargs)


def ul(body=None, **kwargs):
    yield from tag("ul", body, **kwargs)


if __name__ == "__main__":
    import doctest
    doctest.testmod()