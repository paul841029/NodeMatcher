from evaluator.evaluator import Evaluator
from train.method import Naive, NaiveEnsemble

eval = Evaluator("/home/paulluh/CS703_project/matcher/exp/wiki/train",
                 "/home/paulluh/CS703_project/matcher/exp/wiki/test", "wiki-pol-party")
#
# eval = Evaluator("/home/paulluh/CS703_project/matcher/exp/amz/train",
#                  "/home/paulluh/CS703_project/matcher/exp/amz/test", "amz-title")

n = Naive()
for i in range(1, 11):
    eval.train(n, sample_size=i)
    eval.eval(n, "test.csv")
