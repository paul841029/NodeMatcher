from lxml import etree
from os.path import abspath

class Evaluator(object):
    def __init__(self, train, test):
        self.train_file = train
        self.test_file = test

    def _file_name_to_tree(self, file):
        trees = []
        dataset = abspath(file).split('/')[-2]
        with open(file, "r") as mata:
            for file_name in mata.readlines():
                file_name = file_name.strip()
                with open("/home/paulluh/CS703_project/matcher/data/%s/html/%s" % (dataset, file_name)) as f:
                    trees.append(
                        etree.parse(f)
                    )
        return trees

    def train(self, train_method):
        train_trees = self._file_name_to_tree(self.train_file)
        train_method.fit(train_trees)

    def eval(self, train_method, output_file=None):
        test_trees = self._file_name_to_tree(self.test_file)
        tp, fp, fn = train_method.predict(test_trees)

        p, r, f = 0, 0, 0

        try:
            p = tp / (tp + fp)
        except:
            pass
        try:
            r = tp / (tp + fn)
        except:
            pass
        try:
            f = 2 * p * r / (p + r)
        except:
            pass

        if output_file is None:
            print(p, r, f)
