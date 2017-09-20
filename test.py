import requests
import re

user_agent = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'
headers = {'User-Agent': user_agent}
url = 'https://sz.lianjia.com/zufang/rs/'
response = requests.get(url, headers=headers)
print(response.url)
page_num = re.findall(r'https://\S+/zufang/pg(\S*)/', response.url)
if page_num:
    page_num = int(page_num[0])
else:
    page_num = 1
next_page = response.url[0: 30] + 'pg' + str(page_num + 1) + '/'
print(next_page)
print(page_num)