import os
import re
import platform
import subprocess
import urllib.request
import zipfile
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def get_chrome_version():
    """获取当前安装的 Chrome 浏览器版本。"""
    system = platform.system()
    if system == "Darwin":  # macOS
        cmd = "/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --version"
    elif system == "Windows":  # Windows
        cmd = 'reg query "HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon" /v version'
    else:  # Linux
        cmd = "google-chrome --version"
    
    try:
        stream = os.popen(cmd)
        version_output = stream.read().strip()
        match = re.search(r"(\d+\.\d+\.\d+\.\d+)", version_output)
        return match.group(1) if match else None
    except Exception as e:
        print(f"无法检测 Chrome 版本: {e}")
        return None
    
def check_chromedriver_installed():
    """ 检查是否已安装 ChromeDriver. """
    if platform.system() == "Darwin":  # macOS
        chromedriver_path = "/usr/local/bin/chromedriver"
    elif platform.system() == "Windows":  # Windows
        chromedriver_path = "C:\\chromedriver\\chromedriver.exe"
    else:  # Linux
        chromedriver_path = "/usr/local/bin/chromedriver"
    
    return os.path.exists(chromedriver_path)

def download_chromedriver(version):
    # 构造下载 ChromeDriver 的 URL
    base_url = "https://chromedriver.storage.googleapis.com/"
    download_url = f"{base_url}{version}/chromedriver_win32.zip"  # Windows 下载链接
    
    if platform.system() == "Darwin":  # macOS
        download_url = f"{base_url}{version}/chromedriver_mac64.zip"
    elif platform.system() == "Linux":  # Linux
        download_url = f"{base_url}{version}/chromedriver_linux64.zip"
    
    try:
        print(f"正在从 {download_url} 下载 ChromeDriver...")
        zip_path = "chromedriver.zip"
        urllib.request.urlretrieve(download_url, zip_path)
        
        # 解压下载的 ChromeDriver
        print("正在解压 ChromeDriver...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(".")
        
        # 解压后删除 zip 文件
        os.remove(zip_path)
        print(f"ChromeDriver 下载并解压完成。")
        
        # 将 chromedriver 移动到系统可访问的位置
        if platform.system() == "Darwin":
            os.rename("chromedriver", "/usr/local/bin/chromedriver")
        elif platform.system() == "Windows":
            os.rename("chromedriver.exe", "C:\\chromedriver\\chromedriver.exe")
        elif platform.system() == "Linux":
            os.rename("chromedriver", "/usr/local/bin/chromedriver")
        
        # 确保 chromedriver 可执行
        os.chmod("chromedriver", 0o755)
        
    except Exception as e:
        print(f"下载 ChromeDriver 时出错: {e}")