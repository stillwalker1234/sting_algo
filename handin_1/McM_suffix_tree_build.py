"""
Author: Jonas Tranberg 2017
"""
from util import print_tree


def built_tree(_str, verbose=False):
    """
    params:
    _str: input _string

    returns:
    suffix tree, T: list where each element is a list of
        [
          children: list of nodes,
          ancestor: node in tree,
          range of incoming edge: tuple, (start, end),
          s_ptr (list)
        ]

        if children is []] -> node is a terminal node,
        if ancestor is None -> node is root node
    """

    def get_head(node):
        if node is None or node[2] is None:
            return ""
        else:
            return get_head(node[1]) + _str[node[2][0]:node[2][1]]

    def fastscan(node, __str):
        if __str == "":
            return node, node[2][0]
        
        for child in node[0]:
            c_str = _str[child[2][0]:child[2][1]]
            if __str[0] == c_str[0]:
                if len(c_str) <= len(__str):
                    return fastscan(child, __str[len(c_str):])
                else:
                    return slowscan(child[1], __str)
            
    def slowscan(node, __str):
        if verbose:
            print("q: %s" % __str)

        scan_node = node
        position = scan_node[2][0]

        if __str != "":
            for child in node[0]:
                full_match = False

                for k, i in enumerate(range(*child[2])):
                    if k >= len(__str) or _str[i] != __str[k]:
                        full_match = False
                        break
                    else:
                        if full_match:
                            continue
                        else:
                            full_match = True
                            scan_node = child
                
                if full_match:
                    if(len(__str) == k + 1):
                        return scan_node, scan_node[2][0]
                    else:
                        return slowscan(child, __str[k + 1:])
                
                # partial match
                if i != child[2][0]:
                    position = i
                    break

        if verbose:
            print("scan_node: %s, position: %i" % (''.join([_str[j] for j in range(*scan_node[2])]),position))

        return scan_node, position
    
    def add_terminal(node, range):
        node[0].append([[], node, range, None])

    def add_inner(node_add, position):
        ancestor = node_add[1]
        new_node = [[node_add], ancestor, (node_add[2][0], position), None]
        ancestor[0] = [i for i in ancestor[0] if i[2] != node_add[2]]
        ancestor[0].append(new_node)
        node_add[2] = (position, node_add[2][1])
        node_add[1] = new_node

        return new_node

    # build init tree
    T = [[[[], None, (0, len(_str)), None]], None, (0, 0), None]
    T[0][0][1] = T
    T[3] = T

    head_old = T
    head_new = None
    
    tail = _str
    
    # iterate
    for i in range(1, len(_str)):
        if verbose:
            print("===============::============")
        
        empty_head = head_old[2][0] == 0 and head_old[2][1] == 0

        u = None if empty_head else head_old[1]
        v = "" if empty_head else _str[head_old[2][0]:head_old[2][1]]
        w = None

        if u is not None and (u[2][1] - u[2][0]) > 0:
            w, position = fastscan(u[3], v)
        else:
            w, position = fastscan(T, v[1:])
        
        if position != w[2][0]:
            head_new = add_inner(w, position)
            w = head_new
        else:
            head_tmp, position = slowscan(w, tail[1:] if empty_head else tail)

            if position != head_tmp[2][0]:
                head_new = add_inner(head_tmp, position)
            else:
                head_new = head_tmp
        
        head_old[3] = w
        add_terminal(head_new, (len(get_head(head_new)) + i, len(_str)))

        if verbose:
            print_tree(T, _str)

        tail = _str[i+len(get_head(head_new)):]
        head_old = head_new

    return T
