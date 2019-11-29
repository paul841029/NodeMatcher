from evaluator.evaluator import Evaluator
from train.method import Naive

# eval = Evaluator("/home/paulluh/CS703_project/matcher/exp/wiki/train",
#                  "/home/paulluh/CS703_project/matcher/exp/wiki/test", "wiki-pol-party")

eval = Evaluator("/home/paulluh/CS703_project/matcher/exp/amz/train",
                 "/home/paulluh/CS703_project/matcher/exp/amz/test", "amz-price")

n = Naive()
eval.train(n)
eval.eval(n)
