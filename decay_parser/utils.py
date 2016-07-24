from copy import deepcopy


def mark_all(decay):
    marked_decay = deepcopy(decay)

    marked_decay.children[0].marked = True
    marked_decay.children[1].marked = True
    marked_decay.children[2].marked = True

    return marked_decay


def get_branches(decay):
    decay = deepcopy(decay)

    branches = {}
    branches['Dp'] = str(decay)

    decay.children[0].marked = True
    branches['Dp_h'] = str(decay)
    decay.children[0].marked = False

    decay.children[1].marked = True
    branches['Dp_l1'] = str(decay)
    decay.children[1].marked = False

    decay.children[2].marked = True
    branches['Dp_l2'] = str(decay)
    decay.children[1].marked = False

    return branches
