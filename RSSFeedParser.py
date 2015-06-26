import gevent
import feedparser
from newspaper import Article
import xml.etree.ElementTree as ET
from lxml import etree
__author__ = 'andrey_prvt'


class FeedParser(object):

    def __init__(self, input, output):
        self.xml_input_path = input
        self.xml_output = output

    def get_rss_urls(self):
        urls = []
        tree = ET.parse(self.xml_input_path)
        root = tree.getroot()
        for child in root:
            urls.append(child.text)
        return urls

    @staticmethod
    def make_list(lst):
        url_list = []
        for e in lst:
            url_list.append(e)
            if len(url_list) > 4:
                return url_list
        return url_list

    @staticmethod
    def get_urls_from_rss(url, test_mode):
        if test_mode == 1:
            return "empty"
        d = feedparser.parse(url)
        return FeedParser.make_list(d.entries)

    @staticmethod
    def get_article_by_url(url):
        article = Article(url, fetch_images=False)
        article.download()
        if url == "empty":
            return "nolist"
        article.parse()
        return article.text

    @staticmethod
    def canonize(source):
        stop_symbols = '.,!?:;-\n\r()'
        stop_words = ('this', 'how', 'the',
                      'and', 'in', 'under',
                      'into', 'before', 'no',
                      'on', 'but', 'a',
                      'that', 'with', 'as',
                      'so', 'to', 'up',
                      'or', 'for', 'who',
                      'what', 'is', 'are',
                      'do', 'does', 'from',
                      'of', 'he', 'she', 'it', 'all',
                      'now', 'photo', 'advertisement')
        return [x for x in [y.strip(stop_symbols) for y in source.lower().split()] if x and (x not in stop_words)]

    @staticmethod
    def gen_shingle(source):
        import binascii
        shingle_len = 5
        out = []
        for i in range(len(source) - (shingle_len - 1)):
            out.append(binascii.crc32(' '.join([x for x in source[i:i + shingle_len]]).encode('utf-8')))
        return out

    @staticmethod
    def compaire(source1, source2):
        same = 0
        if (len(source1) == 0) | (len(source2) == 0):
            return 0
        for i in range(len(source1)):
            if source1[i] in source2:
                same += 1
        return same * 2 / float(len(source1) + len(source2)) * 100

    def write_xml(self, data, count, fd1, url1, fd2, url2, res):
        news = ET.SubElement(data, "newscouple" + str(count))
        ET.SubElement(news, "text1").text = fd1
        ET.SubElement(news, 'url1').text = url1
        ET.SubElement(news, "text2").text = fd2
        ET.SubElement(news, 'url2').text = url2
        ET.SubElement(news, "similarity").text = str(res)
        tree = ET.ElementTree(data)
        tree.write(self.xml_output)
        parser = etree.XMLParser(resolve_entities=False, strip_cdata=False)
        document = etree.parse(self.xml_output, parser)
        document.write(self.xml_output, pretty_print=True, encoding='utf-8')
        return True

    def single_scrapping(self, test_mode):
        url = self.get_rss_urls()
        url1 = url[0]
        url2 = url[1]
        rss_list1 = self.get_urls_from_rss(url1, test_mode)
        rss_list2 = self.get_urls_from_rss(url2, test_mode)
        data = ET.Element("DATA")
        i = 0
        count = 1
        while i < len(rss_list1):
            j = 0
            if test_mode == 1:
                return False
            article1 = self.get_article_by_url(rss_list1[i])
            cmp1 = self.gen_shingle(self.canonize(article1))
            while j < len(rss_list2):
                self.news_compare(data, cmp1, article1, rss_list1[i], rss_list2[j], count)
                count += 1
                j += 1
            i += 1
        return True

    @staticmethod
    def staff_funk():
        lst = ['1', 'url', '2', 'url']
        for ln in lst:
            FeedParser.make_list(lst)
        for lt in lst:
            if lt == 'url':
                return 'url'
        return lst[0]

    def multi_scrapping(self, test_mode):
        url = self.get_rss_urls()
        url1 = url[0]
        url2 = url[1]
        rss_list1 = self.get_urls_from_rss(url1, test_mode)
        rss_list2 = self.get_urls_from_rss(url2, test_mode)
        i = 0
        data = ET.Element("DATA")
        count = 1
        jobs = []
        while i < len(rss_list1):
            j = 0
            if test_mode == 1:
                return False
            article1 = self.get_article_by_url(rss_list1[i])
            cmp1 = self.gen_shingle(self.canonize(article1))
            while j < len(rss_list2):
                jobs.append(gevent.spawn(self.news_compare, data, cmp1, article1, rss_list1[i], rss_list2[j], count))
                count += 1
                j += 1
            i += 1
        gevent.wait(jobs)
        return True

    def news_compare(self, data, cmp1, article1, url1, url2, count):
        article2 = self.get_article_by_url(url2)
        cmp2 = self.gen_shingle(self.canonize(article2))
        res = self.compaire(cmp1, cmp2)
        if res > 0:
            self.write_xml(data, count, article1, url1, article2, url2, res)
        return True

    def choice_mode(self, choice_mark, test_mode):
        if choice_mark == 'm':
            self.multi_scrapping(test_mode)
        if choice_mark == 's':
            self.multi_scrapping(test_mode)
        return True