from nose.tools import assert_equal

from decay_parser import parse_decay
from decay_parser import Decay as D
from decay_parser import Particle as P


def test_basic():
    yield (try_decay,
           'D0 -> K-',
           D(P('D0'), '->', [P('K-')]))
    yield (try_decay,
           'D0 -> K- pi+',
           D(P('D0'), '->', [P('K-'), P('pi+')]))
    yield (try_decay,
           'D0 -> K- pi+ K+',
           D(P('D0'), '->', [P('K-'), P('pi+'), P('K+')]))


def test_charge_conjugation():
    yield (try_decay,
           '[D0 -> K- pi+ K+]CC',
           cc(D(P('D0'), '->', [P('K-'), P('pi+'), P('K+')])))

    yield (try_decay,
           '[D0]CC -> K- pi+ K+',
           D(cc(P('D0')), '->', [P('K-'), P('pi+'), P('K+')]))
    yield (try_decay,
           'D0 -> [K-]CC pi+ K+',
           D(P('D0'), '->', [cc(P('K-')), P('pi+'), P('K+')]))
    yield (try_decay,
           'D0 -> K- [pi+]CC K+',
           D(P('D0'), '->', [P('K-'), cc(P('pi+')), P('K+')]))
    yield (try_decay,
           'D0 -> K- pi+ [K+]CC',
           D(P('D0'), '->', [P('K-'), P('pi+'), cc(P('K+'))]))

    yield (try_decay,
           'D0 -> [K-]CC [pi+]CC [K+]CC',
           D(P('D0'), '->', [cc(P('K-')), cc(P('pi+')), cc(P('K+'))]))
    yield (try_decay,
           '[D0]CC -> [K-]CC [pi+]CC [K+]CC',
           D(cc(P('D0')), '->', [cc(P('K-')), cc(P('pi+')), cc(P('K+'))]))


def test_nested():
    yield (try_decay,
           'D0 -> K- K+ [phi(1020) -> K- K+]CC',
           D(P('D0'), '->', [
                P('K-'),
                P('K+'),
                cc(D(P('phi(1020)'), '->', [P('K-'), P('K+')]))
           ]))

    yield (try_decay,
           'D0 -> K- K+ (phi(1020) -> K+ K-)',
           D(P('D0'), '->', [
                P('K-'),
                P('K+'),
                D(P('phi(1020)'), '->', [P('K+'), P('K-')])
           ]))


def test_marked():
    yield (try_decay,
           'D0 -> ^K- pi+ K+',
           D(P('D0'), '->', [mark(P('K-')), P('pi+'), P('K+')]))

    yield (try_decay,
           'D0 -> ^K- pi+ K+',
           D(P('D0'), '->', [mark(P('K-')), P('pi+'), P('K+')]))

    yield (try_decay,
           'D0 -> ^K- pi+ K+',
           D(P('D0'), '->', [mark(P('K-')), P('pi+'), P('K+')]))

    yield (try_decay,
           'D0 -> ^[K-]CC pi+ K+',
           D(P('D0'), '->', [mark(cc(P('K-'))), P('pi+'), P('K+')]))

    yield (try_decay,
           'D0 -> ^[K- -> pi0 gamma]CC pi+ K+',
           D(P('D0'), '->', [
                mark(cc(D(P('K-'), '->', [P('pi0'), P('gamma')]))),
                P('pi+'),
                P('K+')
           ]))

    yield (try_decay,
           'D0 -> ^[K- -> ^pi0 gamma]CC pi+ K+',
           D(P('D0'), '->', [
                mark(cc(D(P('K-'), '->', [mark(P('pi0')), P('gamma')]))),
                P('pi+'),
                P('K+')
           ]))

    yield (try_decay,
           'D0 -> ^[K- -> ^[pi0]CC gamma]CC pi+ K+',
           D(P('D0'), '->', [
                mark(cc(D(P('K-'), '->', [mark(cc(P('pi0'))), P('gamma')]))),
                P('pi+'),
                P('K+')
           ]))

    yield (try_decay,
           'D0 -> ^[K- -> ^[pi0]CC ^gamma]CC pi+ K+',
           D(P('D0'), '->', [
                mark(cc(D(P('K-'), '->', [mark(cc(P('pi0'))), mark(P('gamma'))]))),
                P('pi+'),
                P('K+')
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
