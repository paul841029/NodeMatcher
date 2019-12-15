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

# for m in [Naive, NaiveEnsemble, AugmentText]:
for i in range(2, eval.total_train_size+1, 2):
    m = eval.adaptive_training([Naive, NaiveEnsemble, AugmentText], sample_size=i)
    n = m()
    eval.train(n)
    eval.eval(n, args.output)
