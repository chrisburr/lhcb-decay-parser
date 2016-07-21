from nose.tools import assert_equal

from decay_parser import parse_decay, particles
from decay_parser import Decay as D
from decay_parser import Particle as P


def test_basic():
    for p in particles:
        yield (try_decay,
               '{p} -> {p} {p}'.format(p=p),
               D(P(p), '->', [P(p), P(p)]))

        yield (try_decay,
               '{p} -> [{p} -> {p} {p}]CC {p}'.format(p=p),
               D(P(p), '->', [cc(D(P(p), '->', [P(p), P(p)])), P(p)]))

        yield (try_decay,
               '{p} -> ^[{p} -> ^{p} {p}]CC ^{p}'.format(p=p),
               D(P(p), '->', [
                    mark(cc(D(P(p), '->', [mark(P(p)), P(p)]))),
                    mark(P(p))
               ]))


def try_decay(decay, result):
    assert_equal(parse_decay(decay), result)
    assert_equal(decay, str(result))


def mark(particle):
    particle.marked = True
    return particle


def cc(particle):
    particle.cc = True
    return particle
