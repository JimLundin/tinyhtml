"""TinyHTML - a simple HTML generator for Python."""

from collections.abc import Callable, Iterable
from enum import StrEnum, auto
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


class Tag(StrEnum):
    """Pre-defined HTML tags."""

    DOCTYPE = auto()
    HTML = auto()
    HEAD = auto()
    BODY = auto()
    TITLE = auto()
    META = auto()
    LINK = auto()
    STYLE = auto()
    SCRIPT = auto()
    HEADER = auto()
    NAV = auto()
    MAIN = auto()
    ARTICLE = auto()
    SECTION = auto()
    ASIDE = auto()
    FOOTER = auto()
    DIV = auto()
    P = auto()
    HR = auto()
    PRE = auto()
    CODE = auto()
    BLOCKQUOTE = auto()
    SPAN = auto()
    A = auto()
    STRONG = auto()
    EM = auto()
    I = auto()  # noqa: E741
    B = auto()
    U = auto()
    SUB = auto()
    SUP = auto()
    BR = auto()
    UL = auto()
    OL = auto()
    LI = auto()
    DL = auto()
    DT = auto()
    DD = auto()
    TABLE = auto()
    CAPTION = auto()
    THEAD = auto()
    TBODY = auto()
    TFOOT = auto()
    TR = auto()
    TH = auto()
    TD = auto()
    FORM = auto()
    LABEL = auto()
    INPUT = auto()
    BUTTON = auto()
    SELECT = auto()
    OPTION = auto()
    TEXTAREA = auto()
    IMG = auto()
    AUDIO = auto()
    VIDEO = auto()
    SOURCE = auto()
    CANVAS = auto()


def render_content(items: Content) -> str:
    """Render the content of an HTML element."""
    if isinstance(items, Primitive):
        return str(items)
    if isinstance(items, Iterable):
        return "".join(render_content(x) for x in items)

    msg = f"Invalid content type: {type(items)}"
    raise TypeError(msg)


def render_attr(key: str, value: Attr) -> str:
    """Render an HTML attribute."""
    name = key.rstrip("_")

    if value is True:
        return f" {name}"
    if value is False or value is None:
        return ""
    if name == "style" and isinstance(value, dict):
        style_str = ";".join(f"{k}:{v}" for k, v in value.items())
        return f' style="{style_str}"'
    return f' {name}="{value}"'


class Element:
    """HTML element."""

    def __init__(
        self,
        tag: Tag,
        *content: Content,
        void: bool = False,
        preserve_whitespace: bool = False,
        **attrs: Attr,
    ) -> None:
        """Initialize an HTML element.

        Args:
            tag: The tag name of the element.
            content: The content of the element.
            void: Whether the element is a void element.
            preserve_whitespace: Whether to preserve whitespace in the element.
            attrs: The attributes of the element.

        """
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
        """Set the content of the element."""
        if self.is_void and content:
            msg = f"Void element <{self.tag}> cannot have content"
            raise ValueError(msg)
        self.content = content
        return self

    def __str__(self) -> str:
        """Render the element as a string."""
        attrs_str = "".join(
            render_attr(k, v) for k, v in self.attrs.items() if v not in (False, None)
        )

        if self.is_void:
            return f"<{self.tag}{attrs_str}/>"

        if not self.content:
            return f"<{self.tag}{attrs_str}></{self.tag}>"

        content_str = render_content(self.content)

        if self.preserve_whitespace:
            return f"<{self.tag}{attrs_str}>\n{content_str}\n</{self.tag}>"

        return f"<{self.tag}{attrs_str}>{content_str}</{self.tag}>"


def element(
    tag: Tag,
    *,
    void: bool = False,
    preserve_whitespace: bool = False,
) -> Callable[..., Element]:
    """Create an HTML element with the given tag name."""

    def wrapper(*content: Content, **attrs: Attr) -> Element:
        return Element(
            tag,
            *content,
            void=void,
            preserve_whitespace=preserve_whitespace,
            **attrs,
        )

    return wrapper


# Pre-defined elements
# Root and Metadata
Html = element(Tag.HTML)
Head = element(Tag.HEAD)
Body = element(Tag.BODY)
Title = element(Tag.TITLE)
Meta = element(Tag.META, void=True)
Link = element(Tag.LINK, void=True)
Style = element(Tag.STYLE, preserve_whitespace=True)
Script = element(Tag.SCRIPT, preserve_whitespace=True)

# Document Sections
Header = element(Tag.HEADER)
Nav = element(Tag.NAV)
Main = element(Tag.MAIN)
Article = element(Tag.ARTICLE)
Section = element(Tag.SECTION)
Aside = element(Tag.ASIDE)
Footer = element(Tag.FOOTER)

# Content Blocks
Div = element(Tag.DIV)
P = element(Tag.P)
Hr = element(Tag.HR, void=True)
Pre = element(Tag.PRE, preserve_whitespace=True)
Code = element(Tag.CODE, preserve_whitespace=True)
Blockquote = element(Tag.BLOCKQUOTE)

# Text Level
Span = element(Tag.SPAN)
A = element(Tag.A)
Strong = element(Tag.STRONG)
Em = element(Tag.EM)
I = element(Tag.I)  # noqa: E741
B = element(Tag.B)
U = element(Tag.U)
Sub = element(Tag.SUB)
Sup = element(Tag.SUP)
Br = element(Tag.BR, void=True)

# Lists
Ul = element(Tag.UL)
Ol = element(Tag.OL)
Li = element(Tag.LI)
Dl = element(Tag.DL)
Dt = element(Tag.DT)
Dd = element(Tag.DD)

# Tables
Table = element(Tag.TABLE)
Caption = element(Tag.CAPTION)
Thead = element(Tag.THEAD)
Tbody = element(Tag.TBODY)
Tfoot = element(Tag.TFOOT)
Tr = element(Tag.TR)
Th = element(Tag.TH)
Td = element(Tag.TD)

# Forms
Form = element(Tag.FORM)
Label = element(Tag.LABEL)
Input = element(Tag.INPUT, void=True)
Button = element(Tag.BUTTON)
Select = element(Tag.SELECT)
Option = element(Tag.OPTION)
Textarea = element(Tag.TEXTAREA, preserve_whitespace=True)

# Media
Img = element(Tag.IMG, void=True)
Audio = element(Tag.AUDIO)
Video = element(Tag.VIDEO)
Source = element(Tag.SOURCE, void=True)
Canvas = element(Tag.CANVAS)
