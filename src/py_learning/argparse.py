import sys
import argparse


def p(s):
    for i in s:
        print(i)
    print(len(s))


c=0
parser = argparse.ArgumentParser(description='description')
parser.add_argument(
    '-c',
    action='store',
    dest='d')

args = parser.parse_args()
print(args)
