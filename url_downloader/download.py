# url_downloader/download.py

import requests
from requests.exceptions import RequestException
import os

class UrlDownloader:
    def __init__(self, base_url, save_path='.'):
        self.base_url = base_url
        self.save_path = save_path
    def download(self, url_suffix=None):
        """
    下载指定URL的资源到本地。

        :param url_suffix: 资源的URL后缀
        :param target_path: 可选，指定保存文件的完整路径，如果不提供则使用save_path和url_suffix作为文件名
    :return: 文件的保存路径，如果发生错误则返回None
    """
        full_url = None
        if url_suffix:
            full_url = url_suffix
        else:
            full_url = self.base_url
        try:
            response = requests.get(full_url, stream=True)
            response_head = response.headers
            content_type = response_head.get('Content-Type')
            if response.status_code == 200:
                # 判断full_url是否以路径分隔符结尾
                if full_url.endswith('/'):
                    # 如果是路径结尾，且Content-Type存在，则根据Content-Type设置文件名
                    if content_type:
                        _, subtype = content_type.split('/', 1)
                        filename = f"download.{subtype}"
                    else:
                        raise ValueError("无法从响应头获取Content-Type")
                else:
                    # 直接使用URL的最后一部分作为文件名
                    filename = full_url.split('/')[-1]
                target_path = os.path.join(self.save_path, filename)
                
                with open(target_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                return target_path
            else:
                print(f"Failed to download. Status code: {response.status_code}")
        except RequestException as e:
            print(f"An error occurred: {e}")
        return None