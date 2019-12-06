from evaluator.evaluator import Evaluator
from train.method import Naive, NaiveEnsemble, AugmentText
from argparse import ArgumentParser

argparser = ArgumentParser()
argparser.add_argument("--dataset", required=True)
argparser.add_argument("--gt", required=True)
argparser.add_argument("--output", required=True)
args = argparser.parse_args()

# eval = Evaluator("/home/paulluh/CS703_project/matcher/exp/wiki/train",
#                  "/home/paulluh/CS703_project/matcher/exp/wiki/test", "wiki-pol-party")
#
eval = Evaluator("/home/paulluh/CS703_project/matcher/exp/%s/train" % args.dataset,
                 "/home/paulluh/CS703_project/matcher/exp/%s/test" % args.dataset, args.gt)

# n = eval.adaptive_training([Naive, NaiveEnsemble, AugmentText])
for m in [Naive, NaiveEnsemble, AugmentText]:
    n = m()
    for i in range(1, eval.total_train_size+1):
        eval.train(n, sample_size=i)
        eval.eval(n, args.output)
