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

Path('adaptive').mkdir(parents=True, exist_ok=True)

with open(args.input, 'r') as f:
    df = read_csv(f)

for mt in ['prec', 'recal', 'f1']:
    lineplot(x='train-size', y=mt, hue='dataset', data=df, alpha=0.8, style='dataset', palette="cubehelix")
    plt.xlabel("# input-example")
    plt.ylabel(mt)
    plt.title("adaptive -- %s" % mt)
    plt.savefig('adaptive/%s.pdf' % mt)
    plt.clf()

