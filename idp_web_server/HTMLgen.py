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

It is an alternative to templating engines, like Jinja.

Pros:
* use familiar python syntax
* use efficient concatenation techniques
* optional indentation

Cons:
* need to use `classes` tag attribute (instead of `class`, due to python parser)

Tutorial:

A tag is created by calling a function of the appropriate name:

>>> print(render(p("text")))
<p>text</p>

Tag attributes are specified using named arguments:

>>> print(render(p("text", classes="s12"))) # notice the use of `classes`
<p class="s12">text</p>

>>> print(render(p("text", classes=None)))
<p>text</p>

>>> print(render(ul(li("text", selected=True))))
<ul><li selected>text</li></ul>

>>> print(render(ul(li("text", selected=False))))
<ul><li>text</li></ul>

>>> print(render(br(id="1")))
<br id="1">

The innerHTML can be a list:

>>> print(render(div(["text", span("item 1"), span("item 2")])))
<div>text<span>item 1</span><span>item 2</span></div>

The innerHTML can also be specified using the `i` parameter,
after the other attributes, to match the order of rendering:

>>> print(render(ul(classes="s12", i=[li("item 1"), li("item 2")])))
<ul class="s12"><li>item 1</li><li>item 2</li></ul>

For debugging your code, you can set global variable `indent` to `True`
in the code below to obtain HTML with tag indentation, e.g.,

<ul>
  <li>
    item 1
  </li>
</ul>.

"""

indent = False


from typing import Iterator, List, Optional, Union

Tag = Iterator[str]

if indent:
    _tab = "  "
    _cr = "\n"
else:
    _tab = ""
    _cr = ""


def render(gen: Tag) -> str:
    return ''.join(gen)


def solo_tag(name: str, ** kwargs) -> Tag:
    """returns a tag without body, e.g. `<br id="1">`

    Args:
        name : name of the tag
        kwargs (Dict[str, Optional[Union[str, bool]]]): attributes of the tag
            The `i` attributes, if present, is actually the innerHtml of the tag

    Yields:
        Tag: a string iterator to be rendered
    """

    kwargs = { k.replace("classes", "class"): v
               for k, v in kwargs.items()
               if v is not None and (type(v) != bool or v)}

    attrs = ""
    for k,v in kwargs.items():
        if type(v) == bool:
                attrs += f' {k}'
        else:
                attrs += f' {k}="{v}"'

    yield f"<{name}{attrs}>{_cr}"


def tag(name: str,
        body: Optional[Union[str, Tag, List[Union[str, Tag]]]] = None,
        **kwargs
        ) -> Tag:
    """returns a generator of strings, to be rendered as a HTML tag of type `name`

    Args:
        name : name of the tag
        body : body of the tag, or None
        kwargs (Dict[str, Optional[Union[str, bool]]]): attributes of the tag
            The `i` attributes, if present, is actually the innerHtml of the tag

    Yields:
        Tag: a string iterator to be rendered
    """
    if 'i' in kwargs:
        body = kwargs['i']
        del kwargs['i']

    yield from solo_tag(name, **kwargs)

    if body is not None:
        if type(body) == str:  # body is a str
            yield f"{_tab}{body}{_cr}"
        else:
            for b in body:
                if type(b) == str:  # body is a Tag
                    yield f"{_tab}{b}"
                else:  # body is a List[Tag]
                    for b1 in b:
                        yield f"{_tab}{b1}"

    yield f"</{name}>{_cr}"


# in alphabetic order

def a(body=None, **kwargs):
    yield from tag("a", body, **kwargs)


def br(**kwargs):
    yield from solo_tag("br", **kwargs)


def div(body=None, **kwargs):
    yield from tag("div", body, **kwargs)


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