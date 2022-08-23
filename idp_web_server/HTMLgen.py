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

It is an alternative to templating engine, like Jinja.

Pros:
* use familiar python syntax
* use efficient concatenation techniques

Cons:
* the resulting string has no indentation, making it less readable
* need to use `classes` tag attribute (instead of `class`, due to python parser)


Examples:

>>> print(render(p("text")))
<p>text</p>

>>> print(render(p("text", classes="s12"))) # notice the use of `classes`, not `class`
<p class="s12">text</p>

>>> print(render(p("text", classes=None)))
<p>text</p>

>>> print(render(ul(li("text", selected=True))))
<ul><li selected>text</li></ul>

>>> print(render(ul(li("text", selected=False))))
<ul><li>text</li></ul>

>>> print(render(ul([li("item 1"), li("item 2")])))
<ul><li>item 1</li><li>item 2</li></ul>

The inner html can be specified using the `i` parameter:

>>> print(render(ul(classes="s12", i=[li("item 1"), li("item 2")])))
<ul class="s12"><li>item 1</li><li>item 2</li></ul>

"""

from typing import Iterator, List, Optional, Union

Tag = Iterator[str]

def render(gen: Tag) -> str:
    return ''.join(gen)


def tag(name: str,
        body: Optional[Union[Tag, List[Tag]]] = None,
        **kwargs
        ) -> Tag:
    """returns a generator of strings, to be rendered as a HTML tag

    Args:
        name : name of the tab
        body : body of the tag (possibly a list of string generator), or None
        kwargs (Dict[str, Optional[Union[str, bool, List[Tag]]]]): attributes of the tag
            The `i` attributes, if present, is actually the innerHtml of the tag

    Yields:
        Tag: a string iterator to be rendered
    """
    if 'i' in kwargs:
        body = kwargs['i']
        del kwargs['i']

    yield f"<{name}"
    for k,v in kwargs.items():
        if v is not None:
            k = k.replace("classes", "class")
            if type(v) == bool:
                if v:
                    yield f' {k}'
            else:
                    yield f' {k}="{v}"'

    if body is None:
        yield "/>"
    else:
        yield ">"
        try:
            for b in body:
                yield from b
        except:
            yield from body

        yield f"</{name}>"

# in alphabetic order

def a(body=None, **kwargs):
    yield from tag("a", body, **kwargs)


def div(body=None, **kwargs):
    yield from tag("div", body, **kwargs)


def li(body=None, **kwargs):
    yield from tag("li", body, **kwargs)


def p(body=None, **kwargs):
    yield from tag("p", body, **kwargs)


def ul(body=None, **kwargs):
    yield from tag("ul", body, **kwargs)


if __name__ == "__main__":
    import doctest
    doctest.testmod()