from evaluator.evaluator import Evaluator
from train.method import Naive

eval = Evaluator("/home/paulluh/CS703_project/matcher/exp/wiki/train",
                 "/home/paulluh/CS703_project/matcher/exp/wiki/test", "wiki-pol-party")

n = Naive()
eval.train(n)
eval.eval(n)
