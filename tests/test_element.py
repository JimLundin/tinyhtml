"""Testing the Element class."""
from tinyhtml import Element, Tag


def test_element() -> None:
    """Test the Element class."""
    assert(
        str(Element(Tag.HTML, Element(Tag.BODY, Element(Tag.P, "Hello, world!")))) == "<html><body><p>Hello, world!</p></body></html>"
    )