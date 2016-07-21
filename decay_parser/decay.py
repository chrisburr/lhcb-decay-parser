from .particle import Particle


class Decay(Particle):
    def __init__(self, name, search_type, children, cc=False, marked=False):
        super(Decay, self).__init__(name, cc=cc, marked=marked)
        self.children = children
        self.search_type = search_type

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, children):
        self._children = children

    @property
    def search_type(self):
        return self._search_type

    @search_type.setter
    def search_type(self, search_type):
        self._search_type = search_type

    def __str__(self):
        def convert_child(child):
            if isinstance(child, Decay) and not child.cc:
                return '(' + str(child) + ')'
            else:
                return str(child)

        return (
            ['', '^'][self.marked] + ['', '['][self.cc] + self.name + ' ' +
            self.search_type + ' ' +
            ' '.join(map(convert_child, self.children)) + ['', ']CC'][self.cc]
        )

    def __repr__(self):
        return (
            'Decay(' + self.name + ', ' + self.search_type + ', ' +
            repr(self.children) + ', ' + str(self.cc) + ')'
        )
