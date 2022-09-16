# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from itemadapter import ItemAdapter
from scrapy.utils.project import get_project_settings as settings
from .items import RetiDataItem
from dataclasses import asdict

class CrawlDataPipeline:
    def process_item(self, item, spider):
        return item

class MongoDBPipeline:
    def __init__(self):
        conn = pymongo.MongoClient(
            settings().get('MONGO_HOST'),
            settings().get('MONGO_PORT')
        )
        db = conn[settings().get('MONGO_DB_NAME')]
        self.collection = db[settings()['MONGO_COLLECTION_NAME']]

    def process_item(self, item, spider):
        if isinstance(item, RetiDataItem): # article item
            self.collection.insert_one(asdict(item))
        return item