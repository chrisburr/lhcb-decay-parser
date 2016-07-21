from nose.tools import assert_equal

from decay_parser import parse_decay
from decay_parser import Decay as D
from decay_parser import Particle as P


def test_basic():
    yield (try_decay,
           'a -> b',
           D(P('a'), '->', [P('b')]))
    yield (try_decay,
           'a -> b c',
           D(P('a'), '->', [P('b'), P('c')]))
    yield (try_decay,
           'a -> b c d',
           D(P('a'), '->', [P('b'), P('c'), P('d')]))


def test_charge_conjugation():
    yield (try_decay,
           '[a -> b c d]CC',
           cc(D(P('a'), '->', [P('b'), P('c'), P('d')])))

    yield (try_decay,
           '[a]CC -> b c d',
           D(cc(P('a')), '->', [P('b'), P('c'), P('d')]))
    yield (try_decay,
           'a -> [b]CC c d',
           D(P('a'), '->', [cc(P('b')), P('c'), P('d')]))
    yield (try_decay,
           'a -> b [c]CC d',
           D(P('a'), '->', [P('b'), cc(P('c')), P('d')]))
    yield (try_decay,
           'a -> b c [d]CC',
           D(P('a'), '->', [P('b'), P('c'), cc(P('d'))]))

    yield (try_decay,
           'a -> [b]CC [c]CC [d]CC',
           D(P('a'), '->', [cc(P('b')), cc(P('c')), cc(P('d'))]))
    yield (try_decay,
           '[a]CC -> [b]CC [c]CC [d]CC',
           D(cc(P('a')), '->', [cc(P('b')), cc(P('c')), cc(P('d'))]))


def test_nested():
    yield (try_decay,
           'a -> b k [cc -> d]CC',
           D(P('a'), '->', [P('b'), P('k'), cc(D(P('cc'), '->', [P('d')]))]))

    yield (try_decay,
           'a -> b k (cc -> d)',
           D(P('a'), '->', [P('b'), P('k'), D(P('cc'), '->', [P('d')])]))


def test_marked():
    yield (try_decay,
           'a -> ^b c d',
           D(P('a'), '->', [mark(P('b')), P('c'), P('d')]))

    yield (try_decay,
           'a -> ^b c d',
           D(P('a'), '->', [mark(P('b')), P('c'), P('d')]))

    yield (try_decay,
           'a -> ^b c d',
           D(P('a'), '->', [mark(P('b')), P('c'), P('d')]))


def try_decay(decay, result):
    assert_equal(parse_decay(decay), result)
    assert_equal(decay, str(result))


def mark(particle):
    particle.marked = True
    return particle


def cc(particle):
    particle.cc = True
    return particle
