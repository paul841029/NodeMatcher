from pprint import pformat
class Model(object):
    def __call__(self, tree):
        pass

class Xpath(Model):
    def __init__(self, xpath):
        self.xpath = xpath

    def __call__(self, tree):
        return set(tree.xpath(self.xpath))

    def __str__(self):
        return "Naive xpath: %s" % self.xpath

class XpathEnsemble(Model):
    def __init__(self, xpath):
        self.xpath = xpath

    def __call__(self, tree):
        extracted = set()
        for x in self.xpath:
            extracted |= set(tree.xpath(x))
        return extracted

    def __str__(self):
        return" Ensemble: %s " % pformat(self.xpath)





