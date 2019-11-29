class Graph(object):
    def __init__(self):
        self.sources = []

    def add_source_node(self, node):
        self.sources.append(node)