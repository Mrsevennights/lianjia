import time, queue
from URLManager import UrlManager
from DATAOutput import DataOutput
from multiprocessing import Process
from multiprocessing.managers import BaseManager

class Controler:
    def start(self, task_queue, result_queue, url_queue):
        BaseManager.register('task_queue', callable=lambda: task_queue)
        BaseManager.register('result_queue', callable=lambda: result_queue)
        BaseManager.register('url_queue', callable=lambda: url_queue)
        manager = BaseManager(address=('', 8001), authkey=b'lianjia')
        return manager

    def url_manager_proc(self, task_queue, url_queue, root_urls):
        url_manager = UrlManager()
        url_manager.add_new_urls(root_urls)
        while True:
            if url_manager.has_new_url():
                new_url = url_manager.get_new_url()
                if new_url == 'end':
                    print('爬虫爬取完成')
                    return
                print('url: %s放入任务队列' % new_url)
                task_queue.put(new_url)
            if not url_queue.empty():
                url_manager.add_new_url(url_queue.get())


    def save_result_proc(self, result_queue):
        data_output = DataOutput()
        while True:
            while not result_queue.empty():
                item = result_queue.get()
                print('存储结果: %s' % str(item))
                data_output.process_item(item)
            if result_queue.empty():
                time.sleep(5)
                if result_queue.empty():
                    print('爬虫结束')
                    data_output.process_close()
                    return


if __name__ == '__main__':
    control = Controler()
    manager = control.start(queue.Queue(), queue.Queue(), queue.Queue())
    manager.start()
    task_queue = manager.task_queue()
    result_queue = manager.result_queue()
    url_queue = manager.url_queue()
    url_manager_proc = Process(target=control.url_manager_proc, args=(task_queue, url_queue,
                                                              ['https://bj.lianjia.com/zufang/rs/',
                                                               'https://gz.lianjia.com/zufang/rs/',
                                                               'https://sz.lianjia.com/zufang/rs/'],))
    save_result_proc = Process(target=control.save_result_proc, args=(result_queue,))
    url_manager_proc.start()
    save_result_proc.start()
    url_manager_proc.join()
    save_result_proc.join()
    print('爬虫退出')