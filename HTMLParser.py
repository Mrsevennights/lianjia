import re
from lxml import etree

class HtmlParser:
    items = []
    def parser(self, response):
        try:
            tree = etree.HTML(response.text)
            house_list = tree.xpath('//ul[@id="house-lst"]/li')
            for house in house_list:
                title = ''.join(house.xpath('./div[2]/h2/a/text()'))
                link = ''.join(house.xpath('./div[2]/h2/a/@href'))
                house_type = ''.join(house.xpath('.//span[@class="zone"]/span/text()'))
                area = ''.join(house.xpath('./div[2]/div[1]/div[1]/span[2]/text()'))
                direction = ''.join(house.xpath('./div[2]/div[1]/div[1]/span[3]/text()'))
                description = ''.join(house.xpath('./div[2]/div[1]/div[2]/div')[0].xpath('string(.)'))
                tags = ''.join(house.xpath('./div[2]/div[1]/div[3]/div/div')[0].xpath('string(.)'))
                rent = ''.join(house.xpath('./div[2]/div[2]/div[1]/span/text()'))
                time = ''.join(house.xpath('./div[2]/div[2]/div[2]/text()'))
                has_seen = ''.join(house.xpath('./div[2]/div[3]/div/div[1]/span/text()'))
                self.items.append({'title': title, 'link': link, 'house_type': house_type, 'area': area,
                                   'direction': direction, 'description': description, 'tags': tags,
                                   'rent': rent, 'time': time, 'has_seen': has_seen})
            page_num = re.findall(r'https://\S+/zufang/pg(\S*)/', response.url)
            if page_num:
                page_num = int(page_num[0])
            else:
                page_num = 1
            if page_num > 100:
                next_page = 'end'
            else:
                next_page = response.url[0: 30] + 'pg' + str(page_num + 1) + '/'
            return self.items, next_page
        except:
            print(response.status_code)