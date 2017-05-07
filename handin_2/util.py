import sys
from ast import literal_eval as tuple_from_str


def print_tree(node, _str):
    # Add size
    size = 0
    num_nodes = 0

    def _print_sub(_node, depth, size, num_nodes):
        size += sys.getsizeof(node)
        num_nodes += 1
        print(('_' * depth) + str(_node[4]) + " : " + _str[_node[2][0]:_node[2][1]] + " : " + (str(_node[3]) if not type(_node[3]) is list else ""))
        for n in _node[0]:
            _print_sub(n, depth+1, size, num_nodes)

    _print_sub(node, 0, size, num_nodes)


def compare_tandem_repeats_result(grund_truth, result, _str):
    gt_brn, rlt_brn = [grund_truth, set(), set()], [result, set(), set()]

    def _add(_set):
        for line in _set[0]:
            if "branching" in line:
                _value, _type = line.split(' ')
                if "non" in _type:
                    _set[1].add(_value)
                else:
                    _set[2].add(_value)
            else:
                print(line)
    
    _add(gt_brn)
    print()
    _add(rlt_brn)

    def _print(elem):
        i, j, rep = tuple_from_str(elem)
        print(_str[i:i+(j*rep)])
        print(elem + "\n")

    print("\nfalse pos, non")
    for i in rlt_brn[1] - gt_brn[1]:
        _print(str(i))

    print("\nfalse neg, non")
    for i in gt_brn[1] - rlt_brn[1]:
        _print(str(i))

    print("\nfalse pos")
    for i in rlt_brn[2] - gt_brn[2]:
        _print(str(i))

    print("\nfalse neg")
    for i in gt_brn[2] - rlt_brn[2]:
        _print(str(i))

