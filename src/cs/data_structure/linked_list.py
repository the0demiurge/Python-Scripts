#! /usr/bin/env python3
'''This is my learning code for data structure.
This file including Node and linked list.
'''

import warnings


class Node(object):

    """Create a node for a graph"""

    def __init__(self, data=None):
        self.__data = data
        self.__next = []

    @property
    def data(self):
        return self.__data

    def set_data(self, data):
        self.__data = data

    def add(self, next):
        if next not in self.__next:
            self.__next.append(next)
        else:
            warnings.warn('This node is already in next_nodes[]!')

    def remove(self, next):
        if next in self.__next:
            self.__next.remove(next)
        else:
            raise IndexError('This node is not in next_nodes[]!')

    @property
    def next(self):
        ret = []
        for n in self.__next:
            ret.append(n)
        return ret


def test_node():
    n0 = Node('n0')
    nx1 = Node('nx1')
    nx2 = Node('nx2')
    nx3 = Node('nx3')
    n0.add(nx1)
    n0.add(nx2)
    print(n0.next)
    print(n0.data)

    try:
        n0.remove(nx3)
    except IndexError:
        print('Node remove test passed')

    n0.add(nx1)


class LinkList(object):

    """Link list"""

    def __init__(self, lst=None):
        if lst is None:
            lst = []
        self.__head = Node()
        p = self.__head
        for item in lst:
            n = Node(item)
            p.add(n)
            p = n
