from lxml import etree
from os.path import abspath
from pprint import pprint
from random import sample
from loguru import logger
from csv import DictWriter


class Evaluator(object):
    def __init__(self, train, test, gt_tag):
        self.train_file = train
        self.test_file = test
        self.gt_tag = gt_tag
        self.dataset = None
        self.train_size = None

        with open(train, "r") as f:
            self.total_train_size = len(list(f.readlines()))

    def _file_name_to_tree(self, file, sample_size=None):
        trees = []
        dataset = abspath(file).split('/')[-2]
        self.dataset = dataset
        with open(file, "r") as mata:
            filenames = list(mata.readlines())

            if sample_size is not None and sample_size < len(filenames):
                sampled_files = sample(filenames, sample_size)
                logger.info("Sampling %s train files" % sample_size)
            else:
                sampled_files = filenames

            for file_name in sampled_files:
                file_name = file_name.strip()
                with open("/home/paulluh/CS703_project/matcher/data/%s/html/%s" % (dataset, file_name)) as f:
                    trees.append(
                        etree.parse(f, etree.HTMLParser())
                    )
        return trees

    def train(self, train_method, sample_size=None):
        train_trees = self._file_name_to_tree(self.train_file, sample_size)
        self.train_size = len(train_trees)
        train_method.fit(train_trees, self.gt_tag)

    def adaptive_training(self, models):
        train_trees = self._file_name_to_tree(self.train_file)
        train = train_trees[:int(len(train_trees) / 2)]
        val = train_trees[int(len(train_trees) / 2):]

        model = None
        f1_score = 0

        for m in models:
            m_obj = m()
            m_obj.fit(train, self.gt_tag)
            _, _, f = self.get_prf(*m_obj.predict(val, self.gt_tag))
            if f > f1_score:
                f1_score = f
                model = m

        return model

    def get_prf(self, tp, fp, fn):
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

        return p, r, f

    def eval(self, train_method, output_file=None):
        test_trees = self._file_name_to_tree(self.test_file)
        tp, fp, fn = train_method.predict(test_trees, self.gt_tag)
        p, r, f = self.get_prf(tp, fp, fn)
        output_stats = {
            "prec": p,
            "recal": r,
            "f1": f,
            "method": str(train_method),
            "gt-tag": self.gt_tag,
            "dataset": self.dataset,
            "train-size": self.train_size,
            "test-size": len(test_trees)
        }
        if output_file is None:
            pprint(output_stats, indent=4)
        else:

            try:
                with open(output_file, "r") as f:
                    has_header = True
            except FileNotFoundError:
                has_header = False

            with open(output_file, "a+") as f:
                dw = DictWriter(f, fieldnames=[
                    'dataset',
                    'gt-tag',
                    'train-size',
                    'test-size',
                    'method',
                    'prec',
                    'recal',
                    'f1'
                ])
                if not has_header:
                    dw.writeheader()
                dw.writerow(
                    output_stats
                )
