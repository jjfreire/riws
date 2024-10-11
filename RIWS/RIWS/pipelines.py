# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import json

class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open('jobs.json', 'w')
        self.file.write('[')
        self.first_item = True

    def close_spider(self, spider):
        self.file.write(']\n')
        self.file.close()
    
    def process_item(self, item, spider):
        if not self.first_item:
            self.file.write(',\n')
        self.first_item = False
        line = json.dumps(dict(item), indent=4)
        self.file.write(line)
        return item
