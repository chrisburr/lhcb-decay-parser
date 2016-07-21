from __future__ import print_function

import os
import json

from .decay import Decay
from .particle import Particle
from .parser import make_parser


__all__ = [
    'Decay',
    'Particle',
    'parse_decay',
    'particles',
    'symbols'
]


def parse_decay(decay_string):
    result = parser.parseString(decay_string, parseAll=True)
    assert len(result) == 1
    return result[0]


data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))

with open(os.path.join(data_path, 'particles.json')) as f:
    particles = json.load(f)

with open(os.path.join(data_path, 'symbols.json')) as f:
    symbols = json.load(f)

parser = make_parser(particles, symbols)
