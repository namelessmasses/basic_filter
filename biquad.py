#!/usr/bin/python

class Coeffs(object):
    def __init__(self, b0, b1, b2, a1, a2):
        self.b0 = b0
        self.b1 = b1
        self.b2 = b2
        self.a1 = a1
        self.a2 = a2

class State(object):
    def __init__(self, n_1, n_2):
        self.n_1 = n_1
        self.n_2 = n_2

def simple_biquad_direct_form_2(xn, coeffs, w):
    wn = xn - coeffs.a1 * w.n_1 - coeffs.a2 * w.n_2
    yn = coeffs.b0 * wn + coeffs.b1 * w.n_1 + coeffs.b2 * w.n_2
    w.n_2 = w.n_1
    w.n_1 = wn
    return yn

def biquad_direct_form_2(xs, coeffs, w):
    result = [simple_biquad_direct_form_2(xn, coeffs, w) for xn in xs]

    return (w, result)

def biquad_array(xs, coeffs, w):
    coeffsobj = Coeffs(coeffs[0], coeffs[1], coeffs[2], coeffs[3], coeffs[4])
    wobj = State(w[0], w[1])

    wres, result = biquad_direct_form_2(xs, coeffsobj, wobj)
    w[0] = wres.n_1
    w[1] = wres.n_2
    return (w, result)

def biquad_casc(xs, nsections, coeffs, w):
    coeffsIndex = 0
    wIndex = 0
    result = xs
    for section in range(nsections):
        (wres, result) = biquad_array(result,
                                      coeffs[coeffsIndex:coeffsIndex + 5],
                                      w[wIndex:wIndex + 2])
        coeffsIndex += 5
        wIndex += 2

    return (w, result)

if True: #__name__ == '__main__':
    import scipy.signal

    coeffs = Coeffs(0.9988550915,
                    -1.997710183,
                    0.9988550915,
                    -1.997707986,
                    0.9977123799)

    state = State(0, 0)
    
    xs = [168070.000000,
          677268864.000000,
          1194115200.000000,
          1259501952.000000,
          703671040.000000,
          407145440.000000,
          1010275456.000000,
          1693606912.000000,
          1702877312.000000,
          745024256.000000]
    print('{' + ',\n'.join([str(x) for x in xs]) + '}')
    print

    (state, ys) = biquad_direct_form_2(xs, coeffs, state)
    print('\n'.join([str(i) for i in zip(xs, ys)]))
    print
    
    b = [coeffs.b0, coeffs.b1, coeffs.b2]
    a = [1, coeffs.a1, coeffs.a2]
    ys = scipy.signal.lfilter(b, a, xs)

    print('\n'.join([str(i) for i in zip(xs, ys)]))
    print

    impulse = [1.] * 32
    (state, ys) = biquad_direct_form_2(impulse, coeffs, state)
    
    print('\n'.join([str(i) for i in zip(impulse, ys)]))
    print

    coeffs_ary = [
        0.9988550915,	-1.997710183,	0.9988550915, -1.997707986,	0.9977123799,
        0.9457015038,	-1.853079478,	0.9079350529,	-1.853079478,	0.8536365567,
        1.013963262,	-1.896024842,	0.8966433865,	-1.896024842,	0.9106066486,
        0.9424769262,	-1.499103004,	0.8256873229,	-1.499103004,	0.7681642491
        ]

    w_ary = [
        0, 0,
        0, 0,
        0, 0,
        0, 0
        ]

    (w_ary, result) = biquad_casc(xs, 4, coeffs_ary, w_ary)
    print('\n'.join([str(i) for i in zip(xs, result)]))
    print
