#!/usr/bin/env python
from __future__ import print_function

from collections import namedtuple
import json

import PartProp.PartPropSvc  # NOQA
from GaudiPython.Bindings import AppMgr
from PartProp.decorators import Decays, LHCb, Symbols
Nodes = Decays.Nodes


class SymbolDef(namedtuple('S', ['name', 'func', 'description', 'cc'])):
    def __new__(_cls, name, func, description='', cc=True):
        return super(SymbolDef, _cls).__new__(
            _cls, name, lambda pid: func(LHCb.ParticleID(pid)), description, cc
        )


def get_valid_symbols():
    """Get a dictionary of symbols

    As I can't figure out how to extract this from the database just check the
    names and descriptions haven't changed.
    """
    symbol_definitions = {
        "X": SymbolDef('X', Nodes.Any(), "Any particle"),

        "Hadron": SymbolDef('Hadron', Nodes.Hadron(), "Any hadron"),
        "Meson": SymbolDef('Meson', Nodes.Meson(), "Any meson"),
        "Baryon": SymbolDef('Baryon', Nodes.Baryon(), "Any baryon"),
        "Nucleus": SymbolDef('Nucleus', Nodes.Nucleus(), "Any nucleus"),
        "Lepton": SymbolDef('Lepton', Nodes.Lepton(), "Any lepton"),
        "l": SymbolDef('l', Nodes.Ell(), "Any charged lepton"),
        "l+": SymbolDef('l+', Nodes.EllPlus(), "Any positive lepton", "l-"),
        "l-": SymbolDef('l-', Nodes.EllMinus(), "Any negative lepton", "l+"),
        "Nu": SymbolDef('Nu', Nodes.Nu(), "Any neutral lepton"),
        "Neutrino": SymbolDef('Neutrino', Nodes.Nu(), "Any neutral lepton"),

        "X0": SymbolDef('X0', lambda p: True if p.pid() in (10022, 20022) else Nodes.Neutral()(p), "Any neutral particle"),  # NOQA JIRA LHCBGAUSS-770
        "Xq": SymbolDef('Xq', lambda p: False if p.pid() in (10022, 20022) else Nodes.Charged()(p), "Any charged particle"),  # NOQA JIRA LHCBGAUSS-770
        "X+": SymbolDef('X+', lambda p: False if p.pid() in (10022, 20022) else Nodes.Positive()(p), "Any positive particle", "X-"),  # NOQA JIRA LHCBGAUSS-770
        "X-": SymbolDef('X-', lambda p: False if p.pid() in (10022, 20022) else Nodes.Negative()(p), "Any negative particle", "X+"),  # NOQA JIRA LHCBGAUSS-770

        "Xd": SymbolDef('Xd', LHCb.ParticleID.hasDown, "Any particle with d-quark"),  # NOQA
        "Xu": SymbolDef('Xu', LHCb.ParticleID.hasUp, "Any particle with u-quark"),  # NOQA
        "Xs": SymbolDef('Xs', LHCb.ParticleID.hasStrange, "Any particle with s-quark"),  # NOQA
        "Xc": SymbolDef('Xc', LHCb.ParticleID.hasCharm, "Any particle with c-quark"),  # NOQA
        "Xb": SymbolDef('Xb', LHCb.ParticleID.hasBottom, "Any particle with b-quark"),  # NOQA
        "Xt": SymbolDef('Xt', LHCb.ParticleID.hasTop, "Any particle with t-quark"),  # NOQA

        "Down": SymbolDef('Down', LHCb.ParticleID.hasDown, "Any particle with d-quark"),  # NOQA
        "Up": SymbolDef('Up', LHCb.ParticleID.hasUp, "Any particle with u-quark"),  # NOQA
        "Strange": SymbolDef('Strange', LHCb.ParticleID.hasStrange, "Any particle with s-quark"),  # NOQA
        "Charm": SymbolDef('Charm', LHCb.ParticleID.hasCharm, "Any particle with c-quark"),  # NOQA
        "Bottom": SymbolDef('Bottom', LHCb.ParticleID.hasBottom, "Any particle with b-quark"),  # NOQA
        "Beauty": SymbolDef('Beauty', LHCb.ParticleID.hasBottom, "Any particle with b-quark"),  # NOQA
        "Top": SymbolDef('Top', LHCb.ParticleID.hasTop, "Any particle with t-quark"),  # NOQA

        "Scalar": SymbolDef('Scalar', Nodes.JSpin(1), "Any scalar particle j=0"),  # NOQA
        "Spinor": SymbolDef('Spinor', Nodes.JSpin(2), "Any spinor particle j=1/2"),  # NOQA
        "OneHalf": SymbolDef('OneHalf', Nodes.JSpin(2), "Any spinor particle j=1/2"),  # NOQA
        "Vector": SymbolDef('Vector', Nodes.JSpin(3), "Any vector particle j=1"),  # NOQA
        "ThreeHalf": SymbolDef('ThreeHalf', Nodes.JSpin(4), "Any particle with spin j=3/2"),  # NOQA
        "Tensor": SymbolDef('Tensor', Nodes.JSpin(5), "Any tensor particle j=2"),  # NOQA
        "FiveHalf": SymbolDef('FiveHalf', Nodes.JSpin(6), "Any particle with spin j=5/2"),  # NOQA

        "ShortLived": SymbolDef('ShortLived', Nodes.ShortLived_(), "Any short-ilved particle"),  # NOQA
        "LongLived": SymbolDef('LongLived', Nodes.LongLived_(), "Any long-lived particle"),  # NOQA
        "Stable": SymbolDef('Stable', Nodes.Stable(), "Any 'stable' particle"),
        "StableCharged": SymbolDef('StableCharged', Nodes.StableCharged(), "Any 'trackable' particle: stable & charged")  # NOQA
    }

    if len(list(Symbols)) != len(symbol_definitions):
        raise Exception(len(list(Symbols)), len(symbol_definitions))
    for s in Symbols:
        if s not in symbol_definitions:
            raise Exception(s, symbol_definitions)
        if symbol_definitions[s].description != Symbols.symbol(s):
            raise Exception(symbol_definitions[s].description, Symbols.symbol(s))

    return symbol_definitions


Particle = namedtuple('Particle', [
    'name',
    'cc',
    'mass',  # MeV
    'charge',  # e
    'lifetime',  # ns
    'width',
    'pdg_id',
    'pythia_id'
])


Symbol = namedtuple('Symbol', [
    'name',
    'cc',
    'description',
    'contained'
])

# addCC ( "cc"          )
# addCC ( "CC"          )
# addCC ( "os"          )
# addCC ( "nos"         )
# addCC ( "HasQuark"    )
# addCC ( "JSpin"       )
# addCC ( "LSpin"       )
# addCC ( "SSpin"       )
# addCC ( "ShortLived"  )
# addCC ( "LongLived"   )
# addCC ( "ShortLived_" )
# addCC ( "LongLived_"  )
# addCC ( "Stable"      )
# addCC ( "Light"       )
# addCC ( "Heavy"       )
# addCC ( "CTau"        )
# addCC ( "Mass"        )
# addCC ( "up"          )
# addCC ( "down"        )
# addCC ( "strange"     )
# addCC ( "charm"       )
# addCC ( "beauty"      )
# addCC ( "bottom"      )
# addCC ( "top"         )


if __name__ == '__main__':
    # Find the valid particles
    particles = {}
    for p in AppMgr().ppSvc():
        try:
            antiparticle = p.antiParticle().particle()
        except ReferenceError:
            antiparticle = None

        particles[p.particle()] = Particle(
            name=p.particle(),
            cc=antiparticle,
            mass=p.mass(),
            charge=p.charge(),
            lifetime=p.lifetime(),
            width=p.width(),
            pdg_id=p.pdgID().pid(),
            pythia_id=p.pythiaID()
        )

    # Find the valid symbols
    symbols = {}
    for name, func, description, cc in get_valid_symbols().values():
        symbols[name] = Symbol(
            name=name,
            cc=cc,
            description=description,
            contained=[p.name for p in particles.values() if func(p.pdg_id)]
        )

    with open('particles.json', 'wt') as f:
        json.dump(particles, f)

    with open('symbols.json', 'wt') as f:
        json.dump(symbols, f)
