from lxml import etree
from model.graph import Graph


class Parser(object):
    def __init__(self, file_path):
        self.xml_tree = None

        self._load_etree(file_path)

    def _load_etree(self, file_path):
        with open(file_path) as f:
            self.xml_tree = etree.parse(f)

    def parse(self):
        graph = Graph()
        return graph
