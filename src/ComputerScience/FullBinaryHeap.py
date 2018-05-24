from dsr import BinaryTreeNode


class FullBinaryTreeHeap(object):
    def __init__(self, data=None,  is_largest=True):
        self.__is_largest = is_largest
        if is_largest:
            self.__judgement = lambda x, y: x < y
        else:
            self.__judgement = lambda x, y: x > y
        if data is None:
            self.__heap = list()
        else:
            self.__heap = [i for i in data]
            self.heapify()

    def shift_down(self, i):
        child = 2 * i + 1
        T = self.__heap[i]
        while child < len(self.__heap):
            if child + 1 < len(self.__heap) and self.__judgement(
                    self.__heap[child],
                    self.__heap[child + 1]):
                child += 1
            if self.__judgement(T, self.__heap[child]):
                self.__heap[i] = self.__heap[child]
                i = child
                child = 2 * i + 1
            else:
                break
        self.__heap[i] = T

    def shift_up(self, i):
        parent = (i + 1) // 2 - 1
        T = self.__heap[i]
        while parent >= 0:
            if self.__judgement(self.__heap[parent], T):
                self.__heap[i] = self.__heap[parent]
                i = parent
                parent = (i + 1) // 2 - 1
            else:
                break
        self.__heap[i] = T

    def push(self, data):
        self.__heap.append(data)
        self.shift_up(len(self.__heap) - 1)

    def pop(self):
        if len(self.__heap) == 0:
            raise IndexError('No enough data to pop')
        ret = self.__heap[0]
        self.__heap[0] = self.__heap[-1]
        self.__heap.pop()
        if len(self.__heap) > 0:
            self.shift_down(0)
        return ret

    def replace(self, i, data):
        self.__heap[i] = data
        self.shift_up(i)

    def heapify(self):
        for i in range(len(self.__heap) // 2 - 1, -1, -1):
            self.shift_down(i)

    @property
    def data(self):
        return self.__heap.copy()

    @property
    def tree(self):
        return self.__tree()

    def __tree(self, i=None):
        if not self.__heap:
            return BinaryTreeNode()
        if i is None:
            i = 0
        root = BinaryTreeNode(self.__heap[i])
        if 2 * i + 1 < len(self.__heap):
            root.left = self.__tree(2 * i + 1)
        if 2 * i + 2 < len(self.__heap):
            root.right = self.__tree(2 * i + 2)
        return root

    def copy(self):
        return FullBinaryTreeHeap(self.__heap, self.__is_largest)

    def __repr__(self):
        return repr(self.tree)

    def __len__(self):
        return self.__heap.__len__()

    def __iter__(self):
        iterator = self.copy()
        while len(iterator) > 0:
            yield iterator.pop()
