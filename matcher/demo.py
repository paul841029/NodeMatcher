from os.path import abspath
from lxml import etree
from csv import DictWriter
from loguru import logger
from evaluator.evaluator import Evaluator
from train.method import Naive, NaiveEnsemble, AugmentText

class DemoDriver(object):
    def __init__(self, file):
        self.test_file = file

    def run_demo(self, fields):

        dataset = abspath(self.test_file).split('/')[-2]
        self.dataset = dataset

        with open(self.test_file, "r") as mata:
            filenames = list(mata.readlines())

            logger.info("Start extracting attributes for %s documents from %s" % (len(filenames), self.test_file))

            sampled_files = filenames

            with open('amz_demo.csv', 'w', newline='') as csvfile:
                fieldnames = ['amz-title', 'amz-price']
                writer = DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for file_name in sampled_files:
                    file_name = file_name.strip()
                    with open("/home/paulluh/CS703_project/matcher/data/%s/html/%s" % (dataset, file_name)) as f:
                        tree = etree.parse(f, etree.HTMLParser())
                        prod_attr = {}
                        for (field_name, trained_model) in fields:
                            if list(trained_model(tree)) != [] and list(trained_model(tree))[0].text is not None:
                                content = list(trained_model(tree))[0].text
                                prod_attr[field_name] = content.strip()
                            if len(trained_model(tree)) > 1:
                                logger.debug(str(list(map(lambda x: x.text, trained_model(tree)))))
                        writer.writerow(prod_attr)

            logger.info("Finish extracting attributes for %s documents" % len(filenames))
            logger.info("Outputting result to 'amz_demo.csv'")

if __name__ == '__main__':
    eval_title = Evaluator("/home/paulluh/CS703_project/matcher/exp/%s/train" % "amz",
                     "/home/paulluh/CS703_project/matcher/exp/%s/test" % "amz", "amz-title")

    eval_price = Evaluator("/home/paulluh/CS703_project/matcher/exp/%s/train" % "amz",
                     "/home/paulluh/CS703_project/matcher/exp/%s/test" % "amz", "amz-price")

    m_title = eval_title.adaptive_training([Naive, NaiveEnsemble, AugmentText])
    m_price = eval_price.adaptive_training([Naive, NaiveEnsemble, AugmentText])

    n_title = m_title()
    n_price = m_price()


    eval_title.train(n_title)
    eval_price.train(n_price)

    demo_driver = DemoDriver("/home/paulluh/CS703_project/matcher/exp/%s/test" % "amz")
    demo_driver.run_demo([("amz-title", n_title.trained_model), ("amz-price", n_price.trained_model)])
