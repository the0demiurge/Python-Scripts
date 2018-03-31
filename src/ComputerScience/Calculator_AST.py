"""Calculator, worte in AST in python
"""
# This could be implemented as string-based big-number calcaulation


def ADD(x, y):
    return str(eval(x) + eval(y))


def SUB(x, y):
    return str(eval(x) - eval(y))


def POW(x, y):
    return str(eval(x) ** eval(y))


def MUL(x, y):
    return str(eval(x) * eval(y))


def DIV(x, y):
    return str(eval(x) / eval(y))


operations = {
    # 'op': [priority, function]
    '+': [1, ADD],
    '-': [1, SUB],
    '*': [2, MUL],
    '/': [2, DIV],
    '^': [3, POW]
}


class TreeNode(object):
    __slots__ = ('val', 'left', 'right')

    def __init__(self, val=None, left=None, right=None):
        self.val, self.left, self.right = val, left, right

    def __repr__(self):
        left, right = ' ', ' '
        if self.left is not None:
            left = repr(self.left) + ' <- '
        if self.right is not None:
            right = ' -> ' + repr(self.right)
        return '(' + left + repr(self.val) + right + ')'


def split_atomic(string):
    """
    @brief      Splits expression to atoms.

    @param      string  The string expression

    @return     list[tuple("TYPE", 'value')]
    """
    # removing useless parens
    while string.startswith('(') and string.endswith(')'):
        string = string[1:-1]
    result = list()
    if not string:
        return result
    head, tail = 0, 0  # head and tail are used for slice number out

    numeric = False  # Stores previous scanned atom type. If numeric changes, the successor atom type will change
    while tail < len(string):
        # if '+' '-' are operators
        if string[tail] in {'+', '-'} and numeric:
            numeric = False
            result.append(('SYMB', string[tail]))
        # elif numbers or '+' '-' are numbers' symbol
        elif (string[tail].isdecimal() or string[tail] is '.') or (string[tail] in {'+', '-'} and not numeric):
            numeric = True
            head = tail
            tail += 1
            while tail < len(string) and (string[tail].isdecimal() or string[tail] is '.'):
                tail += 1
            num = string[head:tail]
            if num in {'+', '-'}:
                num += '1'
            result.append(('NUM', num))
            tail -= 1
        # elif operators or parentheses
        elif string[tail] in {'*', '/', '^', '(', ')'}:
            symb = 'PAREN' if string[tail] in {'(', ')'} else 'SYMB'
            if numeric and string[tail] is '(':
                result.append(('SYMB', '*'))
            numeric = True if string[tail] is ')' else False
            result.append((symb, string[tail]))
        tail += 1
    return result


def ast(atoms):
    """
    @brief      Receives atoms and return an Abstract Syntax Tree
    for a calculator

    @param      atoms  The atoms splitted by split_atomic

    @return     AST Tree Node
    """
    if len(atoms) is 0:
        return
    # Remove useless parens
    if atoms[0][1] is '(' and atoms[-1][1] is ')':
        atoms = atoms[1:-1]

    parens = {
        '(': 1,
        ')': -1
    }
    paren_amounts = 0
    min_prior = 10
    min_prior_index = None

    # find the operator out of parentheses with smallest priority
    for i, data in enumerate(atoms):
        TYPE, TOKEN = data
        # judge weather in parentheses or not
        if TYPE is 'PAREN':
            paren_amounts += parens[TOKEN]

        elif TYPE is 'SYMB' and paren_amounts is 0:
            if operations[TOKEN][0] < min_prior:
                min_prior_index, min_prior = i, operations[TOKEN][0]

    if min_prior_index is None:
        return TreeNode(atoms[0][1])

    left = ast(atoms[:min_prior_index])
    right = ast(atoms[min_prior_index + 1:])
    return TreeNode(atoms[min_prior_index][1], left, right)


def solve(ast_root, DEBUG=False):
    """Traverse the AST and do calculation
    """
    if ast_root is None:
        raise ValueError('AST cannot be None')
    if ast_root.left is ast_root.right is None:
        return ast_root.val
    else:
        if DEBUG:
            left = solve(ast_root.left, DEBUG)
            right = solve(ast_root.right, DEBUG)
            result = operations[ast_root.val][1](left, right)
            print('Calculating:', ast_root.val, ast_root.left, '|', ast_root.right, '=>', left, ast_root.val, right, '=', result)
            return result
        else:
            return operations[ast_root.val][1](solve(ast_root.left), solve(ast_root.right))


def calculator(string): return solve(ast(split_atomic(string)))


def main():
    DEBUG = False
    prompt = ['Expression > ', 'DEBUG > ']
    try:
        while 1:
            string = input(prompt[DEBUG])
            if string.upper().strip() == 'DEBUG':
                DEBUG = not DEBUG
                continue

            if DEBUG:
                print('Atoms      :', list(zip(*split_atomic(string)))[1])
                print('Tree       :', repr(ast(split_atomic(string))))
                # print('PyResult   :', eval(string.replace('^', '**')))
                print('MyResult   :', solve(ast(split_atomic(string)), DEBUG))
            else:
                print('Result:', calculator(string))
    except (EOFError, KeyboardInterrupt):
        exit()


if __name__ == '__main__':
    main()
