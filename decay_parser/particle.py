class Particle(object):
    def __init__(self, name, cc=False, marked=False):
        self.name = name
        self.cc = cc
        self.marked = marked

    def _enable_cc(self):
        if self.cc:
            raise ValueError(self.name, 'has been charge conjugated twice')
        self.cc = True

    def _enable_marked(self):
        if self.marked:
            raise ValueError(self.name, 'has been marked twice')
        self.marked = True

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = str(name)

    @property
    def cc(self):
        return self._cc

    @cc.setter
    def cc(self, cc):
        self._cc = cc

    @property
    def marked(self):
        return self._marked

    @marked.setter
    def marked(self, marked):
        self._marked = marked

    def __str__(self):
        if self.cc:
            prefix, suffix = '[', ']CC'
        else:
            prefix, suffix = '', ''
        return ['', '^'][self.marked] + prefix + self.name + suffix

    def __repr__(self):
        return (
            'Particle(' +
            self.name + ', ' +
            str(self.cc) + ', ' +
            str(self.marked) + ')'
        )

    def __eq__(self, other):
        return all([
            isinstance(other, self.__class__) or isinstance(self, other.__class__),
            self.__dict__ == other.__dict__
        ])

    def __ne__(self, other):
        return not self.__eq__(other)
