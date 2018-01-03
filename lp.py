#!/usr/bin/python3

def simple_lp(state, xs):
    result = []
    result.append(xs[0] + state)
    for i in range(1, len(xs)):
        result.append(xs[i] + xs[i - 1])

    return (xs[-1], result)


if __name__ == '__main__':
    xs = range(1, 11)

    N = len(xs)
    M = N / 2
    state = 0
    
    state, ys = simple_lp(state, xs[:M])
    state, ys2 = simple_lp(state, xs[M:])

    print(ys + ys2)
