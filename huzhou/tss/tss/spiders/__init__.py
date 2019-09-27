# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from scrapy import cmdline
if __name__ == '__main__':
    cmdline.execute("scrapy crawl mydomain".split())
