from algorithms import ba, kmp, naive


def test_algo(algo):
    print(algo("bbba","abbacbbbababacabbbba"))


test_algo(naive)
test_algo(ba)
test_algo(kmp)