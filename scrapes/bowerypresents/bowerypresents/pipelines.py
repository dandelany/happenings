from pymongo import MongoClient

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class AddToMongoDBPipeline(object):
    def open_spider(self, spider):
        self.mongo_client = MongoClient()
        db = self.mongo_client.happenings
        self.mongo_coll = db.events
        return

    def close_spider(self, spider):
        self.mongo_client.close()
        return

    def process_item(self, item, spider):
        self.mongo_coll.insert(dict(item))
        return item

