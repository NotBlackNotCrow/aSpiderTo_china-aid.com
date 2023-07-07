import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import os
import time
import random

# 读取CSV文件
df = pd.read_csv("targetUrls.csv")

# 创建一个请求头字典
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# 配置请求重试和超时
session = requests.Session()
retry = Retry(total=5, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


count = 0
# 遍历每个URL
for url in df["url"]:
    count += 1
    print("第{}个网页：{}".format(count,url))

    # 等待一段随机时间
    time.sleep(random.uniform(0.5, 1))

    # 发起请求，获取网页内容
    response = session.get(url, headers=headers, timeout=10)
    # 解析网页内容
    soup = BeautifulSoup(response.text, "lxml")
    
    # 获取产品名称
    product_name = soup.xpath('//*[@id="page"]/div[4]/div/div/div/div[1]/h1').text
    
    # 创建子文件夹
    os.makedirs(f"results/{product_name}", exist_ok=True)
    
    # 保存HTML文件
    with open(f"results/{product_name}/page.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    
    # 提取所需元素的文本
    element1 = soup.xpath('//*[@id="page"]/div[4]/div/div/div/div[1]/h1').text
    element2 = soup.xpath('//*[@id="post-32672"]/div[1]/span[2]').text
    element3 = soup.xpath('//*[@id="post-32672"]/div[2]/span[2]').text
    element4 = soup.xpath('//*[@id="post-32672"]/div[5]/p').text
    
    # 保存到TXT文件
    with open(f"results/{product_name}/elements.txt", "w", encoding="utf-8") as f:
        f.write(element1 + "\n" + element2 + "\n" + element3 + "\n" + element4)
    
    # 获取图片链接
    img_url = soup.xpath('//*[@id="post-32672"]/div[4]/img')[0]["src"]
    
    # 下载图片
    img_response = requests.get(img_url)
    with open(f"results/{product_name}/image.jpg", "wb") as f:
        f.write(img_response.content)
