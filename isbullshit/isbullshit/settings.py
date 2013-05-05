# Scrapy settings for isbullshit project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'isbullshit'

SPIDER_MODULES = ['isbullshit.spiders']
NEWSPIDER_MODULE = 'isbullshit.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'isbullshit (+http://www.yourdomain.com)'

MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "isbullshit-scrape"
MONGODB_COL = "blogposts"

# ITEM_PIPELINES = ["isbullshit.pipelines.MongoDBStorage"]

