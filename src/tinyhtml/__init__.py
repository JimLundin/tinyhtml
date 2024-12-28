from collections.abc import Iterable
from typing import Self

# Types - using Python 3.14's native forward refs and union operator
type Primitive = str | bytes | int | float | Element
type Content = Primitive | Iterable[Content]
type Attr = str | int | float | bool | None | dict[str, str]

# HTML specification constants
DEFAULT_ATTRS = {
    "script": {"type": "text/javascript"},
    "style": {"type": "text/css"},
    "input": {"type": "text"},
    "meta": {"charset": "utf-8"},
}


class Element:
    def __init__(
        self,
        tag: str,
        *content: Content,
        void: bool = False,
        preserve_whitespace: bool = False,
        **attrs: Attr,
    ) -> None:
        self.tag = tag
        self.is_void = void
        self.preserve_whitespace = preserve_whitespace
        self.attrs = attrs

        if tag in DEFAULT_ATTRS:
            for k, v in DEFAULT_ATTRS[tag].items():
                self.attrs.setdefault(k, v)

        if void and content:
            msg = f"Void element <{tag}> cannot have content"
            raise ValueError(msg)

        self.content = content

    def __call__(self, *content: Content) -> Self:
        if self.is_void and content:
            msg = f"Void element <{self.tag}> cannot have content"
            raise ValueError(msg)
        self.content = content
        return self

    def __str__(self) -> str:
        def render_attr(key: str, value: Attr) -> str:
            name = key.rstrip("_")

            if value is True:
                return f" {name}"
            if value is False or value is None:
                return ""
            if name == "style" and isinstance(value, dict):
                style_str = ";".join(f"{k}:{v}" for k, v in value.items())
                return f' style="{style_str}"'
            return f' {name}="{value}"'

        attrs_str = "".join(
            render_attr(k, v) for k, v in self.attrs.items() if v not in (False, None)
        )

        if self.is_void:
            return f"<{self.tag}{attrs_str}/>"

        if not self.content:
            return f"<{self.tag}{attrs_str}></{self.tag}>"

        def render_content(items: Content) -> str:
            if isinstance(items, Primitive):
                return str(items)
            if isinstance(items, Iterable):
                return "".join(render_content(x) for x in items)

            msg = f"Invalid content type: {type(items)}"
            raise TypeError(msg)

        content_str = render_content(self.content)

        if self.preserve_whitespace:
            return f"<{self.tag}{attrs_str}>\n{content_str}\n</{self.tag}>"

        return f"<{self.tag}{attrs_str}>{content_str}</{self.tag}>"


# Special case for DOCTYPE
def Doctype() -> str:
    return "<!DOCTYPE html>"


# Pre-defined elements
# Root and Metadata
Html = Element("html")
Head = Element("head")
Body = Element("body")
Title = Element("title")
Meta = Element("meta", void=True)
Link = Element("link", void=True)
Style = Element("style", preserve_whitespace=True)
Script = Element("script", preserve_whitespace=True)

# Document Sections
Header = Element("header")
Nav = Element("nav")
Main = Element("main")
Article = Element("article")
Section = Element("section")
Aside = Element("aside")
Footer = Element("footer")

# Content Blocks
Div = Element("div")
P = Element("p")
Hr = Element("hr", void=True)
Pre = Element("pre", preserve_whitespace=True)
Code = Element("code", preserve_whitespace=True)
Blockquote = Element("blockquote")

# Text Level
Span = Element("span")
A = Element("a")
Strong = Element("strong")
Em = Element("em")
I = Element("i")
B = Element("b")
U = Element("u")
Sub = Element("sub")
Sup = Element("sup")
Br = Element("br", void=True)

# Lists
Ul = Element("ul")
Ol = Element("ol")
Li = Element("li")
Dl = Element("dl")
Dt = Element("dt")
Dd = Element("dd")

# Tables
Table = Element("table")
Caption = Element("caption")
Thead = Element("thead")
Tbody = Element("tbody")
Tfoot = Element("tfoot")
Tr = Element("tr")
Th = Element("th")
Td = Element("td")

# Forms
Form = Element("form")
Label = Element("label")
Input = Element("input", void=True)
Button = Element("button")
Select = Element("select")
Option = Element("option")
Textarea = Element("textarea", preserve_whitespace=True)

# Media
Img = Element("img", void=True)
Audio = Element("audio")
Video = Element("video")
Source = Element("source", void=True)
Canvas = Element("canvas")
