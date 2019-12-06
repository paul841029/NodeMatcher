from pandas import read_csv
from seaborn import lineplot
from argparse import ArgumentParser
from pathlib import Path
import matplotlib.pyplot as plt
from os.path import join


argparser = ArgumentParser()
argparser.add_argument("--input")
argparser.add_argument("--dataset")
argparser.add_argument("--gt")
args = argparser.parse_args()

Path(join(args.dataset, args.gt)).mkdir(parents=True, exist_ok=True)

with open(args.input, 'r') as f:
    df = read_csv(f)

for mt in ['prec', 'recal', 'f1']:
    lineplot(x='train-size', y=mt, hue='method', data=df)
    plt.xlabel("# input-example")
    plt.ylabel(mt)
    plt.title("%s -- %s" % (args.gt, mt))
    plt.savefig(join(args.dataset, args.gt, '%s.png' % mt))
    plt.clf()

