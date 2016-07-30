from collections import namedtuple
from functools import wraps

from naga.tools import apply

FuncWrap = namedtuple('FuncWrap', field_names=['fn', 'args', 'kwargs'])


def precompyled(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        return FuncWrap(fn, args, kwargs)

    return inner


def runall(pc_fn):
    if isinstance(pc_fn, FuncWrap):
        return pc_fn.fn(*map(lambda x: runall(x), pc_fn.args),
                        **dict(map(apply(lambda k, v: (runall(k), runall(v))),
                                   pc_fn.kwargs.items())))
    return pc_fn


def main():
    @precompyled
    def foo(x, y=None):
        return x + 2 + (y or 0)

    @precompyled
    def bar(x):
        return x + 4

    @precompyled
    def baz(x):
        return runall(foo(x)) + runall(bar(x))

    print(runall(foo(baz(2), y=bar(2))))


if __name__ == '__main__':
    main()
