__author__ = 'andrey_prvt'
import unittest
from RSSFeedParser import FeedParser
import xml.etree.ElementTree as ET


class TestMylab(unittest.TestCase):

    def test_get_urls_from_xml(self):
        s = FeedParser("src.xml", "output.xml")
        self.assertEqual(s.get_rss_urls(), ["http://feeds.reuters.com/reuters/technologyNews?format=xml",
                                            "http://feeds.reuters.com/reuters/technologyNews?format=xml"])

    def test_canonize(self):
        self.assertEqual(FeedParser.canonize("this is for test"), ['test'])

    def test_gen_shingle(self):
        self.assertEqual(FeedParser.gen_shingle("hello"), [-749573011])

    def test_compare(self):
        self.assertEqual(FeedParser.compaire([-749573011], [-749573011]), 100.0)

    def test_make_list(self):
        self.assertEqual(FeedParser.make_list(['1', '2', '3', '4', '5', '6']), ['1', '2', '3', '4', '5'])

    def test_news_compare(self):
        s = FeedParser("src.xml", "output.xml")
        self.assertEqual(s.news_compare(" ", [-749573011], "blabla", "", "empty", 0), True)

    def test_get_article_by_url(self):
        self.assertEqual(FeedParser.get_article_by_url("empty"), "nolist")

    def test_get_urls_from_rss(self):
        self.assertEqual(FeedParser.get_urls_from_rss("", 1), "empty")

    def test_write_xml(self):
        s = FeedParser("src.xml", "output.xml")
        self.assertEqual(s.write_xml(ET.Element("Data"), "", "", "", "", "", 10), True)

    def test_single_scrapping(self):
        s = FeedParser("src.xml", "output.xml")
        self.assertEqual(s.single_scrapping(1), False)

    def test_multi_scrapping(self):
        s = FeedParser("src.xml", "output.xml")
        self.assertEqual(s.multi_scrapping(1), False)

    def test_choice_mode(self):
        s = FeedParser("src.xml", "output.xml")
        self.assertEqual(s.choice_mode('s', 1), True)

    def test_stuff_funk(self):
        self.assertEqual(FeedParser.staff_funk(), 'url')

if __name__ == "__main__":
    unittest.main()