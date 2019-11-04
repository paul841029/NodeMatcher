import argparse
from parser.parser import Parser

parser = argparse.ArgumentParser()
parser.add_argument('-f', "--input_file")

args = parser.parse_args()
graph = Parser.parse(args.input_file)


