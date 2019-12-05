from evaluator.evaluator import Evaluator
from train.method import Naive, NaiveEnsemble, AugmentText

# eval = Evaluator("/home/paulluh/CS703_project/matcher/exp/wiki/train",
#                  "/home/paulluh/CS703_project/matcher/exp/wiki/test", "wiki-pol-party")
#
eval = Evaluator("/home/paulluh/CS703_project/matcher/exp/amz/train",
                 "/home/paulluh/CS703_project/matcher/exp/amz/test", "amz-price")

# n = AugmentText()

n = eval.adaptive_training([Naive, NaiveEnsemble, AugmentText])()

for i in range(1, eval.total_train_size+1):
    eval.train(n, sample_size=i)
    eval.eval(n, "amz-ensemble.csv")
