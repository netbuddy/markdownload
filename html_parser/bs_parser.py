# html_parser/bs_parser.py

from bs4 import BeautifulSoup
from lxml import etree
import re
import os
from url_downloader.download import UrlDownloader
from urllib.parse import urljoin

class HtmlParser:
    def __init__(self, html_content=None, file_path=None, url_downloader=None):
        """
        初始化HtmlParser对象。
        :param html_content: 字符串形式的HTML内容。
        :param file_path: HTML文件的路径。
        """
        # self.soup = None
        self.root = None
        self.url_downloader = url_downloader
        # 设置recover=True来忽略解析错误
        parser = etree.HTMLParser(recover=True)  # 使用HTMLParser并开启recover模式
        if html_content:
            # self.soup = BeautifulSoup(html_content, 'lxml')
            self.root = etree.fromstring(html_content, parser=parser)
        elif file_path:
            with open(file_path, encoding='utf-8') as f:
                html_content = f.read()
                self.root = etree.fromstring(html_content, parser=parser)

    def extract_text_by_tag(self, tag_name):
        """
        提取指定标签的所有文本内容。
        :param tag_name: 要提取的标签名称。
        :return: 标签内文本内容的列表。
        """
        # 初始化一个列表来存储图片URLs
        img_urls = []

        # 使用XPath来定位需要提取的标签
        element = self.root.xpath('//' + tag_name)[0]

        # 查找所有的<img>标签
        img_elements = element.findall('.//img')

        # 遍历每一个<img>标签，提取'src'属性的值
        for img_element in img_elements:
            src_attribute = img_element.get('src')  # 正确提取'src'属性的值
            if src_attribute is not None:
                # 下载图片并替换为本地路径
                if self.url_downloader:
                    full_url = urljoin(self.url_downloader.base_url, src_attribute)
                    local_path = self.url_downloader.download(full_url)
                    if local_path:
                        #得到文件名
                        img_name = os.path.basename(local_path)
                        img_element.set('src', img_name)
                # img_dir = os.path.join(self.url_downloader.save_path, 'img')
                # 确保图片目录存在
                # if not os.path.exists(img_dir):
                #     os.makedirs(img_dir)
                

        # 将etree.Element转换回字符串
        element_str = etree.tostring(element, encoding='unicode')

        return element_str

    def save_text_to_file(self, tag_name, file_path):
        """
        将指定标签的所有文本内容保存到文件中。
        :param tag_name: 要提取的标签名称。
        :param file_path: 输出文件的路径。
        """
        element_str = self.extract_text_by_tag(tag_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(element_str)