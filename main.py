import os
import subprocess
from bs4 import BeautifulSoup
import argparse
from url_downloader.download import UrlDownloader
from html_parser.bs_parser import HtmlParser
from markdown_parser.markdown_parser import HtmlTagToMarkdownConverter

def check_html_content(file_path):
    """
    检查文件内容是否符合HTML格式。
    使用BeautifulSoup尝试解析文件，如果解析没有抛出异常，
    则认为文件可能是有效的HTML。
    """
    try:
        # 打开文件并尝试使用BeautifulSoup解析
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'lxml')
        # 如果成功解析，返回True
        return True
    except Exception as e:
        # 解析过程中出现异常，可能是非HTML格式或文件读取错误
        print(f"An error occurred while parsing the file: {e}")
        return False

def save_and_convert_to_markdown(article_content, output_dir):
    # 生成临时的HTML文件名
    temp_html_file = os.path.join(output_dir, "article.html")
    
    # 将文章内容保存为HTML文件
    with open(temp_html_file, 'w', encoding='utf-8') as html_file:
        html_file.write(article_content)
    
    # 定义Pandoc命令，确保输出Markdown文件路径包含output_dir
    markdown_output_file = os.path.join(output_dir, "raw.md")
    pandoc_command = ["pandoc", temp_html_file, "--from", "html", "--to", "markdown_strict", "-o", markdown_output_file]
    
    # 调用Pandoc命令进行转换
    try:
        subprocess.run(pandoc_command, check=True)
        print("转换完成，Markdown文件已生成。")
    except subprocess.CalledProcessError as e:
        print(f"Pandoc转换过程中发生错误: {e}")
    
    # 根据需要，可以选择性地删除临时的HTML文件
    os.remove(temp_html_file)
    return markdown_output_file
def main():
    # 创建解析器
    parser = argparse.ArgumentParser(description="Download a file from a URL and save it to a specified location.")
    
    # 添加命令行参数
    parser.add_argument("url", help="The URL of the file to download.")
    parser.add_argument("save_path", help="The path where the file will be saved.")
    
    # 解析参数
    args = parser.parse_args()
    
    downloader = UrlDownloader(args.url, args.save_path)
    saved_file = downloader.download()
    
    # 先检查文件扩展名
    html_extensions = ['.html', '.htm', '.xhtml']
    if any(saved_file.endswith(ext) for ext in html_extensions):
        print("File extension suggests it could be an HTML file.")
    else:
        print("File extension does not suggest it's an HTML file.")
        # 再检查文件内容
        if check_html_content(saved_file):
            print("Content analysis confirms it is an HTML file.")
        else:
            print("content does not confirm.")
            exit(1)

    parser = HtmlParser(file_path=saved_file, url_downloader=downloader)
    article_content = parser.extract_text_by_tag('article')
    markdown_output_file = save_and_convert_to_markdown(article_content, args.save_path)
    with open(markdown_output_file, 'r', encoding='utf-8') as file:
        markdown_content = file.read()
        converter = HtmlTagToMarkdownConverter(markdown_content)
        processed_markdown = converter.convert()
        with open(os.path.join(args.save_path, "article.md"), 'w', encoding='utf-8') as file1:
            file1.write(processed_markdown)

if __name__ == '__main__':
    main()