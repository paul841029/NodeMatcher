from .model import Xpath
class Train(object):
    def fit(self, train_trees, gt_tag):
        raise NotImplemented

    def predict(self, test_trees, gt_tag):
        raise NotImplemented


class Naive(Train):
    def __init__(self):
        self.trained_model = None

    def fit(self, train_trees, gt_tag):
        xpath_candidate = set()

        for t in train_trees:
            node = t.xpath("//*[@gt='%s']" % gt_tag)[0]
            xpath = "/%s" % node.tag
            parent = node.getparent()
            while parent is not None:
                xpath = "/%s" % parent.tag + xpath
                parent = parent.getparent()
            xpath_candidate.add(xpath)

        if len(xpath_candidate) == 1:
            self.trained_model = Xpath(list(xpath_candidate)[0])

    def predict(self, test_trees, gt_tag):
        tp, fp, fn = 0, 0, 0

        for test in test_trees:

            pred = self.trained_model(test)
            gt_xpath = Xpath(".//*[@gt='%s']" % gt_tag)
            gt = gt_xpath(test)

            tp += len(pred & gt)
            fp += len(pred - gt)
            fn += len(gt - pred)

        return tp, fp, fn
