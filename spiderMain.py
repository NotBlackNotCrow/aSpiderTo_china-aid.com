import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import time
import random
import traceback
import pandas as pd

# 读取CSV文件
df = pd.read_csv("targetUrls.csv")

# 创建一个请求头字典
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"
}

# 非法字符集合
invalid_chars = ["\\", "/", ":", "*", "?", "\"", "<", ">", "|"]

count = 0
lisErrorUrl = []
# 遍历每个URL
for url in df["url"]:
    try:
        count += 1
        print("第{}个网页：{}".format(count,url))

        # 等待一段随机时间
        time.sleep(random.uniform(0.5, 1))

        # 发起请求，获取网页内容
        response = requests.get(url,headers=headers, verify=False)
        # 解析网页内容
        soup = BeautifulSoup(response.text, "lxml")
        

        # 获取产品名称
        product_name = soup.find('h1', {'class': 'entry-title'}).text.strip()
        for char in invalid_chars:
            product_name = product_name.replace(char, "x")

        # 在"result2"文件夹下创建一个以产品名称命名的子文件夹
        os.makedirs(f'result2/{product_name}', exist_ok=True)

        # 保存html文件
        with open(f'result2/{product_name}/{product_name}.html', 'w', encoding='utf-8-sig') as f:
            f.write(response.text)

        # 获取需要保存的文本
        zsnameinfo_text = soup.find('span', {'class': 'zsnameinfo'}).text.strip()
        zstitlen_text = soup.find_all('span', {'class': 'zstitlen'})  # 两次使用这个class获取数据
        entry_content_text = soup.find('div', {'class': 'entry-content'}).text.strip()

        # 在子文件夹中创建txt文件，并将文本保存到文件中
        with open(f'result2/{product_name}/{product_name}.txt', 'w',encoding='utf-8-sig') as f:
            f.write(f"{url}\n{product_name}\n{zsnameinfo_text}\n{entry_content_text}")

        '''    # 获取图片链接
        img_links = soup.find_all('img', {'class': 'lazy-load preload-me'})
        for link in img_links:
            img_url = link.get('data-src')
            img_response = requests.get(img_url, headers=headers, stream=True, timeout=10, verify=False)
            img_response.raise_for_status()
            with open(f'result2/{product_name}/{os.path.basename(img_url)}', 'wb') as f:
                for block in img_response.iter_content(1024):
                    if not block:
                        break
                    f.write(block)'''

        # 获取图片链接
        img_links = soup.find_all('img', {'class': 'lazy-load preload-me'})
        for link in img_links:
            img_url = link.get('data-src')
            img_response = requests.get(img_url, headers=headers, stream=True, timeout=10, verify=False)
            img_response.raise_for_status()

            # 临时保存图片到硬盘
            temp_path = f'result2/{product_name}/{os.path.basename(img_url)}'
            with open(temp_path, 'wb') as f:
                for block in img_response.iter_content(1024):
                    if not block:
                        break
                    f.write(block)

            # 检查图片大小
            img_size = os.path.getsize(temp_path)
            if img_size < 20 * 1024:  # 如果图片小于20KB
                os.remove(temp_path)  # 删除图片
    except (Exception, BaseException) as e :
        print('{:*^60}'.format('出错链接：'))
        print(url)
        lisErrorUrl.append(url)
        print('{:*^60}'.format('具体原因：'))
        print(e)
        print('{:*^60}'.format('错误类型：'))
        print(repr(e))
        print('{:*^60}'.format('具体位置：'))
        exstr = traceback.format_exc()
        print(exstr)

