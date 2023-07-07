import re
import pandas as pd

def extract_all_urls(html):
    pattren = re.compile(r'https://www.china-aid.com/[^\s]+.html')
    url_lst = pattren.findall(html)
    return url_lst

html0 = open(r'D:\AAA_ImportantFiles\files\职业技能\广发产业研究院202302-？\temp\0608数据\view-source_https___www.china-aid.com_recommend.html',encoding='utf-8').read()

print(extract_all_urls(html0))


