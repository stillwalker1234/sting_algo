from McM_suffix_tree_build import built_tree
from tandem_repeat_finder import find_tandem_repeats
from util import analyse
from matplotlib import pyplot as plt
import random


def test_tamdem_repeats_complexity():
    _map = ['a', 'g', 't', 'c']

    def args_generator(n):
        _str = ''.join([_map[random.randint(0, 3)] for _ in range(n)])
        _str += ' '
        return built_tree(_str), _str

    _r = range(20, 1000, 5)

    y = analyse(find_tandem_repeats, args_generator, _r)

    plt.plot(_r, y)
    plt.show()


test_tamdem_repeats_complexity()
