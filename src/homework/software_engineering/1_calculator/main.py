import sys
import math
import re

operations = {
        '(': [1, None],
        ')': [1, None],
        '**': [2, math.pow],
        '/': [3, lambda a, b: a / b],
        '*': [3, lambda a, b: a * b],
        '+': [4, lambda a, b: a + b],
        '-': [4, lambda a, b: a - b],
        }


class stack(list):
    '''create stack, which has pop() and push()
    '''

    def push(self, data):
        self.append(data)

    def top(self):
        return self[-1]


def preparse(arg):

    assert isinstance(arg, str), 'wrong input of arg: %s' % type(arg)
    arg = re.sub('\s+', '', arg)
    operators = re.split('[\d\.]+', arg)
    digits = re.findall('[\d\.]+', arg)

    for index, item in enumerate(operators):
        if re.match('.*[\(\)]', item):
            brackets = re.findall('[\(\)]', item)
            remains = re.split('[\(\)]', item)
            for bracket in brackets:
                remains[remains.index('')] = bracket
            operators[index] = remains

    args = [operators.pop(0)]
    for index, digit in enumerate(digits):
        args.append(digit)
        args.append(operators[index])

    def traverse(tree, result):
        if isinstance(tree, str):
            result.append(tree)
        elif isinstance(tree, list):
            for leaf in tree:
                traverse(leaf, result)
        else:
            print('error travsing trees, data format is not str or list!')
            raise TypeError(type(tree))

    result = []
    traverse(args, result)
    return(result)


def main():
    if len(sys.argv) <= 1:
        print('put in the expression!')
        return
    print(sys.argv[-1], '=', end=' ')
    arg = sys.argv[-1]

    args = preparse(arg)
    for item in args:
        if item is '':
            args.remove('')
    print(args)




if __name__ == '__main__':
    main()
