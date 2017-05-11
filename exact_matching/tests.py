from algorithms import ba, kmp, naive
from matplotlib import pyplot as plt
import timeit
import random


def analyse(func_under_test, args_gen, tests_points, number=5, multiple_args=True):
    """

    :param func_under_test: the function to measure
    :param args_gen: function that returns tuple of args to func_under_test
    :param tests_points: x-axis
    :param number: number repeats to create the test point average
    :return: y-axis, time given args_gen(test point)
    """
    result = []

    global current_args
    global f
    f = func_under_test

    for k in tests_points:
        agg_value = 0.
        for j in range(number):
            current_args = args_gen(k)
            if multiple_args:
                stm = "f(*current_args)"
            else:
                stm = "f(current_args)"

            agg_value += timeit.timeit(stmt=stm,
                    setup="from " + __name__ + " import f, current_args",
                    number=1)
        result += [agg_value / float(number)]

    return result


def test_algo(algo):
    print(algo("bbba","abbacbbbababacabbbba"))


def test_algo_complexity(algos):
    _map = ['a', 'g', 't', 'c']

    def args_generator(n, max_n=100**2):
        _str = ''.join([_map[random.randint(0, 3)] for _ in range((n//4)+1)])
        _str += ' '

        _str_2 = ''.join([_map[random.randint(0, 3)] for _ in range(n)])
        _str_2 += ' '
        return _str, _str_2

    _r = [i**2 for i in range(20, 400, 10)]

    handles = []
    for i, algo in enumerate(algos):
        y = analyse(algo, args_generator, _r)

        handles.append(plt.plot(_r, y, label=str(i))[0])
    
    plt.legend(handles=handles)

    plt.show()

def test_algo_simple(algos):

    def args_generator(n, max_n=100**2):
        _str = ''.join('a' for _ in range((n)))
        _str_2 = ''.join('a' for _ in range((n/4) + 1))
        return _str, _str_2

    _r = [i**2 for i in range(20, 10000, 10)]

    handles = []
    for i, algo in enumerate(algos):
        y = analyse(algo, args_generator, _r)

        handles.append(plt.plot(_r, y, label=str(i))[0])

    plt.legend(handles=handles)

    plt.show()


if __name__ == "__main__":
    test_algo_complexity([naive, ba, kmp])
    test_algo_simple([naive, ba, kmp])

