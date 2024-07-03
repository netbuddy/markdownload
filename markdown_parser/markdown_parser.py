import re
from bs4 import BeautifulSoup
import os

class HtmlTagToMarkdownConverter:
    """
    一个类，用于将HTML中的<a>和<img>标签转换为Markdown格式的链接和图片描述。
    """
    def __init__(self, text_with_html):
        """
        初始化方法，传入包含HTML片段的文本。
        """
        self.text_with_html = text_with_html

    def _convert_tag_to_markdown(self, match):
        """
        将提取的HTML标签转换为Markdown格式。
        """
        tag_soup = BeautifulSoup(match.group(), 'html.parser')
        
        if tag_soup.find('a'):
            tag = tag_soup.a
            href = tag.get('href', '')
            text = tag.get_text(strip=True)  # 先移除首尾空白并获取文本
            text = text.replace('\n', ' ')  # 将文本中的换行符替换为空格
            return f'[{text}]({href})'
        
        elif tag_soup.find('img'):
            tag = tag_soup.img
            src = tag.get('src', '')
            alt = tag.get('alt', '')  # 如果alt不存在，默认为空字符串
            alt_text = alt if alt else os.path.basename(src)  # 使用文件名为替代
            return f'![{alt_text}]({src})'

    def convert(self):
        """
        执行转换过程。
        """
        a_pattern = re.compile(r'<a\b[^>]*?>.*?</a>', re.DOTALL)
        img_pattern = re.compile(r'<img\b[^>]*?/?>', re.DOTALL)
        while True:
            a_match = a_pattern.search(self.text_with_html)
            img_match = img_pattern.search(self.text_with_html)
            if not a_match and not img_match:
                break
            
            if a_match and (not img_match or a_match.start() < img_match.start()):
                replacement = self._convert_tag_to_markdown(a_match)
                self.text_with_html = self.text_with_html[:a_match.start()] + replacement + self.text_with_html[a_match.end():]
            elif img_match:
                replacement = self._convert_tag_to_markdown(img_match)
                self.text_with_html = self.text_with_html[:img_match.start()] + replacement + self.text_with_html[img_match.end():]
        return self.text_with_html
