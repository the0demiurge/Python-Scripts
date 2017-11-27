import random
from collections import deque


class ReplayBuffer(object):
    """ReplayBuffer for DRL
    Accept for tuple, (state, act, reward, next_state)"""

    def __init__(self, maxlen, data=list()):
        self._maxlen = maxlen
        self._buffer = deque(data, maxlen=maxlen)

    def __len__(self):
        return len(self._buffer)

    def sample(self, batch_size=32):
        if len(self._buffer) <= batch_size:
            return list(self._buffer)
        else:
            return random.sample(self._buffer, batch_size)

    def append(self, data):
        self._buffer.appendleft(data)

    def extend(self, data_list):
        self._buffer.extendleft(data_list)

    def clear(self):
        self._buffer.clear()

    @property
    def content(self):
        return list(self._buffer)

    @property
    def maxlen(self):
        return self._maxlen

    def __repr__(self):
        return self._buffer.__repr__()

    def __str__(self):
        return self._buffer.__str__()


def test_buffer():
    data = [(1, 2, 3)] * 5 + [(2, 3, 4)] * 3
    buffer = ReplayBuffer(7, data)
    print(buffer.content)
    buffer.append((3, 4, 5))
    print(buffer.content)
    buffer.extend([(6, 4, 2)] * 2)
    print(buffer.content, len(buffer))
    print(buffer.sample(3), len(buffer))
    print(buffer.sample(7))
    print(buffer.sample(8))
    buffer.clear()
    print(buffer.content, len(buffer))

