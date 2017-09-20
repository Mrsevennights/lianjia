from HTMLDownloader import HtmlDownloader
from HTMLParser import HtmlParser
from multiprocessing import Pool
from multiprocessing.managers import BaseManager
import time

class Worker:
    def work(self, task_queue, result_queue, url_queue):
        downloader = HtmlDownloader()
        parser = HtmlParser()
        while True:
            while not task_queue.empty():
                new_url = task_queue.get()
                if new_url == 'end':
                    print('爬虫爬取完成')
                    return
                print('获得新任务: %s' % new_url)
                response = downloader.download(new_url)
                items, next_page = parser.parser(response)
                url_queue.put(next_page)
                for item in items:
                    print('任务完成: %s' % item)
                    result_queue.put(item)

if __name__ == '__main__':
    #pool = Pool(10)
    worker = Worker()
    BaseManager.register('task_queue')
    BaseManager.register('result_queue')
    BaseManager.register('url_queue')

    manager = BaseManager(address=('127.0.0.1', 8001), authkey=b'lianjia')
    manager.connect()
    task_queue = manager.task_queue()
    result_queue = manager.result_queue()
    url_queue = manager.url_queue()
    worker.work(task_queue, result_queue, url_queue)
    print('爬虫退出')