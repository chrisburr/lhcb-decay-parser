from .particle import Particle


class Decay(Particle):
    def __init__(self, name, children, cc=False):
        super(Decay, self).__init__(name, cc=cc)
        self.children = children

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, children):
        self._children = children

    def __str__(self):
        if self.cc:
            prefix, suffix = '[', ']CC'
        else:
            prefix, suffix = '(', ')'
        return prefix + self.name + ' -> ' + ' '.join(map(str, self.children)) + suffix
