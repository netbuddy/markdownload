# test_bs_parser.py
import os
import pytest
from bs4 import BeautifulSoup
from html_parser.bs_parser import HtmlParser

html_doc = """
<html>
<head><title>My Web Page</title></head>
<body>
    <article>
        <h1>Welcome to my page</h1>
        <p>This is some text.</p>
        <a href="http://example.com">Example Link</a>
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
        </ul>
    </article>
    <footer>Copyright 2023</footer>
</body>
</html>
"""

# 测试HtmlParser的初始化和extract_text_by_tag方法
class TestHtmlParser:
    @pytest.fixture
    def sample_html_content(self):
        return html_doc
    
    @pytest.fixture
    def sample_html_file(self, tmp_path, sample_html_content):
        file = tmp_path / "sample.html"
        file.write_text(sample_html_content)
        return str(file)

    def test_extract_text_by_tag_with_content(self, sample_html_content):
        parser = HtmlParser(html_content=sample_html_content)
        text = parser.extract_text_by_tag('article')
        assert text == '<article>\n        <h1>Welcome to my page</h1>\n        <p>This is some text.</p>\n        <a href="http://example.com">Example Link</a>\n        <ul>\n            <li>Item 1</li>\n            <li>Item 2</li>\n        </ul>\n    </article>\n    '

    def test_extract_text_by_tag_with_file(self, sample_html_file):
        parser = HtmlParser(file_path=sample_html_file)
        text = parser.extract_text_by_tag('p')
        assert text == '<p>This is some text.</p>\n        '

    def test_save_text_to_file(self):
        parser = HtmlParser(file_path='tests/example1.html')
        text = parser.save_text_to_file('article', '/tmp/article.html')
        assert os.path.exists('/tmp/article.html')
# 钩入pytest
if __name__ == "__main__":
    pytest.main()