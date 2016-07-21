import pyparsing as pp

from .decay import Decay
from .particle import Particle


__all__ = [
    'make_parser'
]


def make_parser(particles, symbols):
    # Make the inputs to the parser
    particle_literals = map(lambda s: pp.Literal(s).setName(s), particles.keys())

    # Make the parser
    element = pp.Forward().setName('Element')

    particle = pp.Or(particle_literals).setName('Particle')
    particle = particle.setParseAction(lambda x: Particle(x[0]))

    decay = element + pp.Or(['->', '-->', '=>']) + pp.OneOrMore(element)
    decay = decay.setParseAction(lambda x: Decay(x[0], x[1], x[2:]))
    decay = decay.setName('Decay')

    element_cc = supress('[', pp.Or([element, decay]), ']CC')
    element_cc = element_cc.setParseAction(lambda x: x[0]._enable_cc() or x[0])

    element << pp.Or([
        supress('(', element, ')'), mark(supress('(', element, ')')),
        supress('(', decay, ')'), mark(supress('(', decay, ')')),
        element_cc, mark(element_cc),
        particle, mark(particle)
    ])

    return pp.Or([decay, element_cc])


def supress(prefix, body, suffix):
    prefix = pp.Literal(prefix).suppress().setName(prefix)
    suffix = pp.Literal(suffix).suppress().setName(suffix)
    return prefix + body + suffix


def mark(obj):
    marked_obj = pp.Literal('^').suppress().setName('^') + obj
    marked_obj = marked_obj.setParseAction(lambda x: x[0]._enable_marked() or x[0])
    return marked_obj
