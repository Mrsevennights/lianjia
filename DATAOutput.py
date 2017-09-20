import json

class DataOutput:
    def __init__(self):
        self.file = open('lianjia.json', 'w')

    def process_item(self, item):
        line = json.dumps(item, ensure_ascii=False) + '\n'
        self.file.write(line)
        print(item)

    def process_close(self):
        self.file.close()