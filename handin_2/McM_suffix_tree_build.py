"""
Author: Jonas Tranberg 2017

Implementation of McCreight's suffix tree construction algorithm

"""
from util import print_tree


def built_tree(_str, verbose=False):
    """
    params:
    _str = input string
    verbose: print stuff?

    returns:
    suffix tree: list where each node is a list of
        [
          children: list of nodes,
          ancestor: node in tree,
          range of incoming edge: tuple, (start, end),
          s_ptr (list) or starting index of suffix if node is a terminal node
        ]

        if children is [] -> node is a terminal node,
        if ancestor is None -> node is the root node
    """

    def get_head(node):
        if node is None or node[2] is None:
            # node[2] None means that there is no ancestors
            return 0
        else:
            # Repeats with getting the ancestor of the current node + the length between the end - start of incoming edges
            return get_head(node[1]) + (node[2][1] - node[2][0])

    def fastscan(node, __str):
        if __str == "":
            # Returns the current node, and the start of the incoming edges
            return node, node[2][0]
        
        for child in node[0]:
            c_str = _str[child[2][0]:child[2][1]]
            # Characters in string from the start to the end index of the incoming edges in the built string
            if __str[0] == c_str[0]:
                #Matches first character
                if len(c_str) <= len(__str):
                    # if the length is less than the length of the total string, it can be expanded
                    return fastscan(child, __str[len(c_str):])
                else:
                    # Returns list of children nodes, and the whole current string
                    return slowscan(child[1], __str)
            
    def slowscan(node, __str):
        if verbose:
            print("q: %s" % __str)

        scan_node = node
        position = scan_node[2][0]

        if __str != "":
            # If the string is not empty, not all children will probably match
            for child in node[0]:
                full_match = False

                for k, i in enumerate(range(*child[2])):
                    # Go through each character in child
                    if k >= len(__str) or _str[i] != __str[k]:
                        # Either the string is longer than the one we are looking at, meaning it can't be full match
                        # Or if the prefix does not match with the string at the current location
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
                        # See if string is one longer than the range of edges coming to the curent child's string
                        return scan_node, scan_node[2][0]
                    else:
                        # Cut off the string at K + 1 and do it again on the child node
                        return slowscan(child, __str[k + 1:])
                
                # partial match
                if i != child[2][0]:
                    position = i
                    break

        if verbose:
            print("scan_node: %s, position: %i" % (''.join([_str[j] for j in range(*scan_node[2])]),position))

        return scan_node, position
    
    def add_terminal(node, _range, i):
        # Add node with no children, the current node as the ancestor, the range and the starting index of suffix
        node[0].append([[], node, _range, i])

    def add_inner(node_add, position):
        ancestor = node_add[1]
        # New node is inserted between the ancestor and the node to add
        new_node = [[node_add], ancestor, (node_add[2][0], position), None]
        # Adding all children to the ancestor as long as the child node's range is not the same as node_add
        ancestor[0] = [i for i in ancestor[0] if i[2] != node_add[2]]
        # Adding new node the ancestor
        ancestor[0].append(new_node)
        # So new range of node_add is its position to its original end point of incoming edges
        node_add[2] = (position, node_add[2][1])
        # Making the ancestor the new inner node
        node_add[1] = new_node

        return new_node


    # build init tree
    T = [[[[], None, (0, len(_str)), 0]], None, (0, 0), None]
    T[0][0][1] = T
    T[3] = T

    head_old = T
    head_new = None
    
    tail = _str
    
    # iterate
    for i in range(1, len(_str)):
        if verbose:
            print("===============::============")

        # Range of starting node
        empty_head = head_old[2] == (0, 0)

        # Ancestor of current node
        u = None if empty_head else head_old[1]
        # v is the string range, taken from the slice of the range of the ancestor node
        v = "" if empty_head else _str[head_old[2][0]:head_old[2][1]]
        w = None

        # Check to make sure range is not (0,0) for example
        if u is not None and (u[2][1] - u[2][0]) > 0:
            # Use fastcan with the string stored at u and the slice of string v
            w, position = fastscan(u[3], v)
        else:
            # Use fastscan with the head node and all but the beginning letter of the string
            w, position = fastscan(T, v[1:])
        
        if position != w[2][0]:
            # If the start position from the scan does not equal the start position of the scanned node
            head_new = add_inner(w, position)
            # Add a node and split the range up, based on the position, continuing with the new inner node
            w = head_new
        else:
            # If it does match, then can do a slowscan
            head_tmp, position = slowscan(w, tail[1:] if empty_head else tail)

            if position != head_tmp[2][0]:
                # Same as above
                head_new = add_inner(head_tmp, position)
            else:
                head_new = head_tmp

        # Get the range of the head to the root, or basically the length, as each ancestor has the number of end - start of edges added
        # But also add the how far into the string we are with + i
        head_new_len = get_head(head_new) + i
        head_old[3] = w
        # Create new terminal node right under the current node, like adding the $ in the string
        add_terminal(head_new, (head_new_len, len(_str)), i)

        if verbose:
            print_tree(T, _str)

        # Take the original string and cut off the characters up to now, since we have gone through them
        tail = _str[head_new_len:]
        head_old = head_new

    return T