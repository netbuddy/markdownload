import pytest
from bs4 import BeautifulSoup
from markdown_parser.markdown_parser import HtmlTagToMarkdownConverter

html_a_multiline_doc = """
# <a
href="https://eli.thegreenplace.net/2024/the-life-of-an-ollama-prompt/"
rel="bookmark" title="Permalink to The life of an Ollama prompt">The
life of an Ollama prompt</a>
"""

html_img_multiline_doc = """
<img
src="https://eli.thegreenplace.net/images/2024/ollama-internals.png"
class="align-center"
alt="Internals of ollama, showing service connecting to clients and loading GGUF" />
"""

def test_convert_a_tag():
    html_text = '<p>This is a <a href="https://example.com">link</a>.</p>'
    expected_output = '<p>This is a [link](https://example.com).</p>'
    converter = HtmlTagToMarkdownConverter(html_text)
    assert converter.convert() == expected_output

def test_convert_a_tag_multiline():
    html_text = html_a_multiline_doc
    expected_output = '\n# [The life of an Ollama prompt](https://eli.thegreenplace.net/2024/the-life-of-an-ollama-prompt/)\n'
    converter = HtmlTagToMarkdownConverter(html_text)
    output = converter.convert()
    assert output == expected_output

def test_convert_img_tag():
    html_text = '<p><img src="image.jpg" alt="Image description"></p>'
    expected_output = '<p>![Image description](image.jpg)</p>'
    converter = HtmlTagToMarkdownConverter(html_text)
    assert converter.convert() == expected_output

def test_convert_img_tag_multiline():
    html_text = html_img_multiline_doc
    expected_output = '\n![Internals of ollama, showing service connecting to clients and loading GGUF](https://eli.thegreenplace.net/images/2024/ollama-internals.png)\n'
    converter = HtmlTagToMarkdownConverter(html_text)
    output = converter.convert()
    assert converter.convert() == expected_output

def test_convert_img_tag_without_alt():
    html_text = '<p><img src="image.jpg"></p>'
    expected_output = '<p>![image.jpg](image.jpg)</p>'
    converter = HtmlTagToMarkdownConverter(html_text)
    assert converter.convert() == expected_output

def test_convert_multiple_tags():
    html_text = '<p>Text with <a href="https://example.com">link</a> and <img src="image.jpg"></p>'
    expected_output = '<p>Text with [link](https://example.com) and ![image.jpg](image.jpg)</p>'
    converter = HtmlTagToMarkdownConverter(html_text)
    assert converter.convert() == expected_output