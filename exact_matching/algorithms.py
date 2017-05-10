def get_border_array(x):
    b_arr = [0] * len(x)
    for i in range(1, len(x)):
        b = b_arr[i-1]
        while b > 0 and x[i] != x[b]:
            b = b_arr[b-1]
        if x[i] == x[b]:
            b_arr[i] = b+1
        else:
            b_arr[i] = 0
    
    return b_arr


def naive(query, _string):
    """
    O(n*m) implementation of Exact Matching
    """
    n = len(_string)
    m = len(query)
    ret = []

    for i in range(n-m+1):
        for j in range(m):
            if _string[i+j] != query[j]:
                break
            elif j == m-1:
                ret.append(i)

    return ret


def ba(query, _string):
    """
    O(n+m) implementation of Exact Matching
    """

    x = [ord(i) for i in query] + [-1] + [ord(i) for i in _string]
    b_arr = get_border_array(x)
    m = len(query)
    return [i-2*m for i in range(len(x)) if b_arr[i] == m]


def kmp(query, _string):
    """
    O(n) implementation of Knuth-Morris-Pratt Exact Matching
    """

    b_arr = get_border_array(query)
    b_arr = [0] + [i for i in b_arr]
    ret = []
    n = len(_string)
    m = len(query)

    def match(i, j):
        while j < m and query[j] == _string[i]:
            i += 1
            j += 1
        return i, j

    i = 0
    j = 0

    while i < n-m+j+1:
        i, j = match(i,j)
        if j == m:
            ret.append(i-m)
        
        if j == 0:
            i += 1
        else:
            j = b_arr[j]
    
    return ret
