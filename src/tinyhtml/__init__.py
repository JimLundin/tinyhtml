from collections.abc import Iterable
from typing import Self

# Types - using Python 3.14's native forward refs and union operator
type Primitive = str | bytes | int | float | Element
type Content = Primitive | Iterable[Content]
type Attr = str | int | float | bool | None

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
        void: bool,
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
            raise ValueError(f"Void element <{tag}> cannot have content")

        self.content = content

    def __call__(self, *content: Content) -> Self:
        if self.is_void and content:
            raise ValueError(f"Void element <{self.tag}> cannot have content")
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
            raise TypeError(f"Invalid content type: {type(items)}")

        content_str = render_content(self.content)

        if self.preserve_whitespace:
            return f"<{self.tag}{attrs_str}>\n{content_str}\n</{self.tag}>"

        return f"<{self.tag}{attrs_str}>{content_str}</{self.tag}>"


# Special case for DOCTYPE
def Doctype() -> str:
    return "<!DOCTYPE html>"


# Pre-defined elements
# Root and Metadata
Html = Element("html", void=False)
Head = Element("head", void=False)
Body = Element("body", void=False)
Title = Element("title", void=False)
Meta = Element("meta", void=True)
Link = Element("link", void=True)
Style = Element("style", void=False, preserve_whitespace=True)
Script = Element("script", void=False, preserve_whitespace=True)

# Document Sections
Header = Element("header", void=False)
Nav = Element("nav", void=False)
Main = Element("main", void=False)
Article = Element("article", void=False)
Section = Element("section", void=False)
Aside = Element("aside", void=False)
Footer = Element("footer", void=False)

# Content Blocks
Div = Element("div", void=False)
P = Element("p", void=False)
Hr = Element("hr", void=True)
Pre = Element("pre", void=False, preserve_whitespace=True)
Code = Element("code", void=False, preserve_whitespace=True)
Blockquote = Element("blockquote", void=False)

# Text Level
Span = Element("span", void=False)
A = Element("a", void=False)
Strong = Element("strong", void=False)
Em = Element("em", void=False)
I = Element("i", void=False)
B = Element("b", void=False)
U = Element("u", void=False)
Sub = Element("sub", void=False)
Sup = Element("sup", void=False)
Br = Element("br", void=True)

# Lists
Ul = Element("ul", void=False)
Ol = Element("ol", void=False)
Li = Element("li", void=False)
Dl = Element("dl", void=False)
Dt = Element("dt", void=False)
Dd = Element("dd", void=False)

# Tables
Table = Element("table", void=False)
Caption = Element("caption", void=False)
Thead = Element("thead", void=False)
Tbody = Element("tbody", void=False)
Tfoot = Element("tfoot", void=False)
Tr = Element("tr", void=False)
Th = Element("th", void=False)
Td = Element("td", void=False)

# Forms
Form = Element("form", void=False)
Label = Element("label", void=False)
Input = Element("input", void=True)
Button = Element("button", void=False)
Select = Element("select", void=False)
Option = Element("option", void=False)
Textarea = Element("textarea", void=False, preserve_whitespace=True)

# Media
Img = Element("img", void=True)
Audio = Element("audio", void=False)
Video = Element("video", void=False)
Source = Element("source", void=True)
Canvas = Element("canvas", void=False)
