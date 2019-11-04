from lxml import etree
from model.graph import Graph
from model.node import Node


class Parser(object):
    def __init__(self, file_path):
        self.xml_tree = None

        self._load_etree(file_path)

    def _load_etree(self, file_path):
        with open(file_path) as f:
            self.xml_tree = etree.parse(f)

    def parse(self):
        node = Node()
        root = self.xml_tree
        node.tag = root.tag
        node.attributes = root.attrib
        graph = Graph()
        graph.add_source_node(node)
        return graph

    def get_next_node(self):
        """
        TODO: Iterator function to perform parsing recursively
        :return:
        """
        pass
