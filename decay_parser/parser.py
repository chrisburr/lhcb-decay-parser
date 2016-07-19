import pyparsing as pp

from .decay import Decay
from .particle import Particle


__all__ = [
    'make_parser'
]


def make_parser():
    element = pp.Forward().setName('Element')

    particle = pp.Word(pp.alphanums).setName('Particle')
    particle = particle.setParseAction(lambda x: Particle(x[0]))

    decay = element + pp.Or(['->', '-->', '=>']) + pp.OneOrMore(element)
    decay = decay.setParseAction(lambda x: Decay(x[0], x[1], x[2:]))
    decay = decay.setName('Decay')

    element_cc = supress('[', pp.Or([element, decay]), ']CC')
    element_cc = element_cc.setParseAction(lambda x: x[0].enableCC() or x[0])

    element << pp.Or([
        supress('(', element, ')'),
        supress('(', decay, ')'),
        element_cc,
        particle
    ])

    return pp.Or([decay, element_cc])


def supress(prefix, body, suffix):
    prefix = pp.Literal(prefix).suppress().setName(prefix)
    suffix = pp.Literal(suffix).suppress().setName(suffix)
    return prefix + body + suffix
