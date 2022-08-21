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
This module contains functions to generate HTML

Example:
> print(render(p("Hello world)))
<p>Hello world</p>
"""

from typing import Iterator, List, Optional, Union


def render(gen: Iterator[str]) -> str:
    return ''.join(gen)


def tag(name: str,
        body: Optional[Union[Iterator[str], List[Iterator[str]]]] = None,
        **kwargs
        ) -> Iterator[str]:
    """creates a generator of strings, to be rendered as a HTML tag

    Args:
        name (str): name of the tab
        body (Iterator[str]): body of the tag (possibly a list of iterators)
        kwargs (Dict[str, Union[str, bool, Iterator[str]]]): attributes of the tag
            The `i` attributes, if present, is actually the innerHtml of the tag

    Yields:
        Iterator[str]: a string iterator to be rendered
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
