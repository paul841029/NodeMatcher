class Node(object):
    def __init__(self):
        self.children = []
        self.previous = None
        self.next = None
        self.tag = None
        self.attributes = None

    def set_tag(self, tag):
        self.tag = tag

    def set_attributes(self, attributes):
        self.attributes = attributes