import itertools
from functools import reduce


class LazySeq(object):
    __slots__ = ['seq', 'cache', 'idx']

    def __init__(self, seq):
        self.seq = iter(seq)
        self.cache = {}
        self.idx = -1

    def __getitem__(self, idx):
        if isinstance(idx, slice):
            return self.__getslice__(idx.start, idx.stop, idx.step)

        elif idx in self.cache:
            return self.cache[idx]
        else:
            while self.idx < idx:
                self.cache[self.idx + 1] = next(self.seq)
                self.idx += 1
            return self[idx]

    def __iter__(self):
        idx = 0
        while True:
            try:
                yield self[idx]
                idx += 1
            except StopIteration:
                raise StopIteration

    def __next__(self):
        return self[0]

    def __add__(self, other):
        return list(self) + list(other)

    def __eq__(self, other):
        return id(self) == id(other)

    def __getslice__(self, start, stop=None, step=None):
        if not stop:
            stop = start
            return list(itertools.islice(self, stop))
        else:
            return list(itertools.islice(self, start, stop, step))

    def append(self, item):
        return self + [item]

    def __contains__(self, item):
        return item in list(self)

    def __reversed__(self):
        return reversed(list(self))

    def __rmul__(self, other):
        return list(self) * other

    def __setitem__(self, idx, value):
        return list(self).__setitem__(idx, value)

    def __setslice__(self, i, j, sequence):
        return list(self).__setslice__(i, j, sequence)

    def __str__(self):
        return 'LazySequence({})'.format(repr(self.seq))

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        i = 0
        for i in self:
            pass
        return i + 1

    def count(self, item):
        return list(self).count(item)

    def extend(self, other):
        return self + other

    def index(self, item):

        for n, _item in enumerate(self):
            if item == _item:
                return n

    def insert(self, idx, item):
        base_list = list(self)
        return base_list[:idx] + [item] + [base_list[idx + 1:]]

    def pop(self, idx=None):
        base_list = list(self)
        if idx is None:
            return base_list[:-1]
        return base_list[:idx] + base_list[idx + 1:]

    def __nonzero__(self):
        try:
            return bool(self[0])
        except IndexError:
            return False
