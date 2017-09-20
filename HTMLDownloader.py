import requests, time, random

class HtmlDownloader:
    def download(self, url):
        if url is None:
            return
        time.sleep(random.random() * 5)
        user_agent = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'
        #proxies = {'https': 'https://219.149.46.151:3129', 'https': 'https://120.78.15.63:80'}
        headers = {'User-Agent': user_agent}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            return response