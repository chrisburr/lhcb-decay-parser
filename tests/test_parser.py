from nose.tools import assert_equal

from decay_parser import parse_decay
from decay_parser import Decay as D
from decay_parser import Particle as P


class CP(P):
    def __init__(self, name):
        super(CP, self).__init__(name, cc=True)


class CD(D):
    def __init__(self, name, children):
        super(CD, self).__init__(name, children, cc=True)


def test_basic():
    yield try_decay, 'a -> b', D(P('a'), [P('b')])
    yield try_decay, 'a -> b c', D(P('a'), [P('b'), P('c')])
    yield try_decay, 'a -> b c d', D(P('a'), [P('b'), P('c'), P('d')])


def test_charge_conjugation():
    yield try_decay, '[a -> b c d]CC', D(P('a'), [P('b'), P('c'), P('d')])

    yield try_decay, '[a]CC -> b c d', D(CP('a'), [P('b'), P('c'), P('d')])
    yield try_decay, 'a -> [b]CC c d', D(P('a'), [CP('b'), P('c'), P('d')])
    yield try_decay, 'a -> b [c]CC d', D(P('a'), [P('b'), CP('c'), P('d')])
    yield try_decay, 'a -> b c [d]CC', D(P('a'), [P('b'), P('c'), CP('d')])

    yield try_decay, 'a -> [b]CC [c]CC [d]CC', D(P('a'), [CP('b'), CP('c'), CP('d')])
    yield try_decay, '[a]CC -> [b]CC [c]CC [d]CC', D(CP('a'), [CP('b'), CP('c'), CP('d')])


def test_nested():
    yield try_decay, 'a -> b c d', D(P('a'), [P('b'), P('c'), P('d')])

    yield try_decay, 'a -> b k [cc -> d]CC', D(
        P('a'),
        [P('b'), P('k'), CD(P('cc'), [P('d')])]
    )

    yield try_decay, 'a -> b k (cc -> d)', D(
        P('a'),
        [P('b'), P('k'), D(P('cc'), [P('d')])]
    )


def try_decay(decay, result):
    assert_equal(parse_decay(decay), result)
