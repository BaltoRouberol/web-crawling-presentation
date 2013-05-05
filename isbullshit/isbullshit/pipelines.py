import pymongo

from scrapy.conf import settings
from scrapy import log


class MongoDBStorage(object):
    def __init__(self):
        """ Initiate a MongoDB connection to the settings['MONGODB_COL'] collection. """
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        db = settings['MONGODB_DB']
        col = settings['MONGODB_COL']
        connection = pymongo.MongoClient(host, port)
        db = connection[db]
        self.collection = db[col]

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        log.msg(
            'Blogpost from %s inserted in database' % (item['url']),
            level=log.DEBUG, spider=spider
        )
        return item
