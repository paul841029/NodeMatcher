from .model import Xpath, XpathEnsemble
from loguru import logger


class Train(object):

    def __init__(self):
        self.trained_model = None

    def fit(self, train_trees, gt_tag):
        raise NotImplemented

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


class Naive(Train):
    def fit(self, train_trees, gt_tag):
        xpath_candidate = set()

        for t in train_trees:
            try:
                node = t.xpath("//*[@gt='%s']" % gt_tag)[0]
                xpath = "/%s" % node.tag
                parent = node.getparent()
                while parent is not None:
                    xpath = "/%s" % parent.tag + xpath
                    parent = parent.getparent()
                xpath_candidate.add(xpath)
            except:
                logger.error("gt not found")

        if len(xpath_candidate) == 1:
            self.trained_model = Xpath(list(xpath_candidate)[0])
        else:
            raise RuntimeError("Inconsistent xpath in candidates")

    def __str__(self):
        return "Tags on path"


class NaiveEnsemble(Train):
    def fit(self, train_trees, gt_tag):
        xpath_candidate = set()
        for t in train_trees:
            try:
                node = t.xpath("//*[@gt='%s']" % gt_tag)[0]
                xpath_candidate.add(t.getpath(node))
            except:
                logger.error("gt not found")

        self.trained_model = XpathEnsemble(list(xpath_candidate))

    def __str__(self):
        return "Ensemble of tags and positions"


class AugmentText(Train):

    def __init__(self, depth=0):
        super().__init__()
        self.depth = depth

    def _text_cleaning(self, text):
        text = text.replace("\n", "")
        text = text.replace("\t", "")
        text = text.replace(" ", "")
        return text

    def fit(self, train_trees, gt_tag):
        xpath_candidate = set()

        for t in train_trees:
            try:
                node = t.xpath("//*[@gt='%s']" % gt_tag)[0]
                xpath = "/%s" % node.tag

                follow_sib_txt_pattern = "[following-sibling::*[%d][text()='%s']]"
                pred_sib_txt_pattern = "[preceding-sibling::*[%d][text()='%s']]"

                next_sib = node.getnext()
                start_idx = 1
                while next_sib is not None:
                    if next_sib.text is not None and self._text_cleaning(next_sib.text) is not '':
                        xpath += follow_sib_txt_pattern % (start_idx, next_sib.text)
                    next_sib = next_sib.getnext()
                    start_idx += 1

                prev_sib = node.getprevious()
                start_idx = 1
                while prev_sib is not None:
                    if prev_sib.text is not None and self._text_cleaning(prev_sib.text) is not '':
                        xpath += pred_sib_txt_pattern % (start_idx, prev_sib.text)
                    prev_sib = prev_sib.getprevious()
                    start_idx += 1

                parent = node.getparent()

                while parent is not None:
                    cur_node = "/%s" % parent.tag
                    depth = self.depth
                    if depth > 0:
                        if parent.text is not None and self._text_cleaning(parent.text) is not '':
                            cur_node += "[text()='%s']" % parent.text
                        depth -= 1

                    xpath = cur_node + xpath
                    parent = parent.getparent()

                xpath_candidate.add(xpath)
            except IndexError:
                logger.error("gt not found")

        if len(xpath_candidate) == 1:
            # print(list(xpath_candidate)[0])
            self.trained_model = Xpath(list(xpath_candidate)[0])
        else:
            print(xpath_candidate)
            raise RuntimeError("Inconsistent xpath in candidates")

    def __str__(self):
        return "Ancestors and siblings and their text attributes"
