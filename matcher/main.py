from evaluator.evaluator import Evaluator
from train.train import Naive

eval = Evaluator("/home/paulluh/CS703_project/matcher/exp/wiki/train",
                 "/home/paulluh/CS703_project/matcher/exp/wiki/test")

n = Naive()
eval.train(n)
eval.eval(n)
