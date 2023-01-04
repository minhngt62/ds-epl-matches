# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import Item
import json

class JsonWriter:
    def open_spider(self, spider):
        self.file = open(spider.output, 'w')
    
    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        record = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(record)
        return item

class PlayerDefaultFields:
    def process_item(self, item: Item, spider):
        for field in item.fields:
            item.setdefault(field, 0)
