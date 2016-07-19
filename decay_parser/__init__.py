from __future__ import print_function

from .decay import Decay
from .particle import Particle
from .parser import make_parser

parser = make_parser()


__all__ = [
    'Decay',
    'Particle',
    'parse_decay'
]


def parse_decay(decay_string):
    result = parser.parseString(decay_string, parseAll=True)
    assert len(result) == 1
    return result[0]
