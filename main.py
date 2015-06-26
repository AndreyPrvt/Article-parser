__author__ = 'andrey_prvt'
from RSSFeedParser import FeedParser
import time


feed_parser = FeedParser("src.xml", "output.xml")

start_time = time.time()
feed_parser.choice_mode('m', 0)
end_time = time.time()

print end_time - start_time