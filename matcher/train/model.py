class Model(object):
    def __call__(self, tree):
        pass

class Xpath(Model):
    def __init__(self, xpath):
        self.xpath = xpath

    def __call__(self, tree):
        return set(tree.xpath(self.xpath))





