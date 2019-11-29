from lxml import etree
from urllib.parse import urljoin
from requests import get
from loguru import logger
from os.path import join
from io import StringIO
from selenium import webdriver

logger.add("logs.log")


class Scraper(object):

    def __init__(self, source, output_file_location):
        self.source = source
        self.output_file_location = output_file_location

    def wiki_get_next_url(self, base_url):
        with open("wiki_source.html", "r") as f:
            tree = etree.parse(f)
        for t in tree.xpath(".//li//a[1]/@href"):
            yield urljoin(base_url, t), t.split('/')[-1]

    def amz_get_next_url(self, base_url):
        with open("amz_source.html", "r") as f:
            tree = etree.parse(f, etree.HTMLParser())
        for t in tree.xpath(".//a[contains(@class, 'a-text-normal')]/@href"):
            yield urljoin(base_url, t), t.split('/')[1]
        # time.sleep(0.5 * random.random())

    def wiki_tag_ground_truth_node(self, node, gt_type):
        if 'gt' not in node.attrib:
            node.attrib['gt'] = gt_type
        else:
            node.attrib['gt'] += " %s" % gt_type

    def wiki_tag_political_party_cell(self, info_box):
        try:
            pol = info_box.xpath(".//th[text()='Political party']/following-sibling::td")[0]
        except IndexError:
            logger.error("Political party cell not found")
            return
        self.wiki_tag_ground_truth_node(pol, "wiki-pol-party")

    def wiki_add_ground_truth(self, info_box):
        self.wiki_tag_political_party_cell(info_box)

    def wiki_extract_info_box(self, url):
        r = get(url)
        tree = etree.fromstring(r.content)
        info_box = tree.xpath(".//table[contains(@class, 'infobox')]")[0]
        self.wiki_add_ground_truth(info_box)

        return etree.tostring(info_box, pretty_print=True)

    def amz_tag_title_span(self, node):
        try:
            t = node.xpath(".//span[@id='productTitle']")[0]
            t.attrib['gt'] = 'amz-title'
        except IndexError:
            logger.error("amz-title not found")

    def amz_tag_price(self, node):
        try:
            t = node.xpath(".//span[contains(@id, 'priceblock_')]")[0]
            t.attrib['gt'] = 'amz-price'
        except IndexError:
            logger.error('amz-price not found')

    def amz_add_ground_truth(self, node):
        self.amz_tag_title_span(node)
        self.amz_tag_price(node)

    def amz_extract(self, url):

        driver = webdriver.Firefox()
        driver.get(url)
        html = driver.page_source
        driver.quit()

        with StringIO(html) as f:
            tree = etree.parse(f, etree.HTMLParser())

        self.amz_add_ground_truth(tree)

        for e in tree.xpath(".//script|.//meta|.//style"):
            e.getparent().remove(e)

        return etree.tostring(tree, pretty_print=True)

    def wiki_run(self):
        with open(join(self.output_file_location, "all_files.txt"), "w") as f:
            pass

        for i, name in self.wiki_get_next_url("https://en.wikipedia.org/"):
            logger.info("processing: %s" % name)

            with open(join(self.output_file_location, "html/%s.html") % name, "w") as f:
                f.write(self.wiki_extract_info_box(i).decode("utf-8"))

            with open(join(self.output_file_location, "all_files.txt"), "a") as f:
                f.write("%s.html\n" % name)

            logger.info("processed: %s" % name)

    def amz_run(self):
        with open(join(self.output_file_location, "all_files.txt"), "w") as f:
            pass

        for idx, (i, name) in enumerate(self.amz_get_next_url("https://www.amazon.com/")):
            logger.info("processing: %s" % name)

            with open(join(self.output_file_location, "html/%s.html") % name, "w") as f:
                f.write(self.amz_extract(i).decode("utf-8"))

            with open(join(self.output_file_location, "all_files.txt"), "a") as f:
                f.write("%s.html\n" % name)

            logger.info("processed: %s" % name)
