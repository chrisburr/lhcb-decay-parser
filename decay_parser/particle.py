class Particle(object):
    def __init__(self, name, cc=False):
        self.name = name
        self.cc = cc

    def enableCC(self):
        if self.cc:
            raise ValueError(self.name, 'has been charge conjugated twice')
        self.cc = True

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

    def __str__(self):
        if self.cc:
            prefix, suffix = '[', ']CC'
        else:
            prefix, suffix = '', ''
        return prefix + self.name + suffix

    def __repr__(self):
        return 'Particle(' + self.name + ', ' + str(self.cc) + ')'

    def __eq__(self, other):
        return all([
            isinstance(other, self.__class__) or isinstance(self, other.__class__),
            self.__dict__ == other.__dict__
        ])

    def __ne__(self, other):
        return not self.__eq__(other)
