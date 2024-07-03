# test_url_downloader.py
import os
import requests
import pytest
from url_downloader.download import UrlDownloader

# 请确保这个URL指向一个确实存在的资源以避免测试失败
TEST_BASE_URL = 'https://blog.codingnow.com/2024/06/game_idea.html'

@pytest.fixture(scope="module")
def downloader():
    """Fixture to create a UrlDownloader instance for tests."""
    return UrlDownloader(TEST_BASE_URL)

def test_download_to_default_location(downloader, tmpdir):
    """
    使用pytest的tmpdir fixture来自动管理临时目录，
    确保每个测试都在干净的环境中运行，且测试后自动清理。
    """
    try:
        # 设置临时保存路径
        downloader.save_path = str(tmpdir)
        target_path = downloader.download()
        
        # 检查文件是否下载成功并存在于预期路径
        assert target_path is not None
        assert os.path.exists(target_path)
        
        # 这里可以进一步检查下载内容是否正确，例如比较文件大小或内容
        
    except requests.RequestException as e:
        pytest.fail(f"Download failed unexpectedly: {e}")
