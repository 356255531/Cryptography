######################## IMPORT MODULES #############################

import os, sys, math, csv, time

###################### USEFUL ROUTINES ##############################


def testBit(val, offset):
    """
    Test whether bit at position offset is set or not
    Returns: 1 if it is set, 0 otherwise
    """
    if (val & (1 << offset)) != 0:
        return bool(1)
    else:
        return bool(0)


def testPair(testing_pair, d, n):
    """
    Test whether the provided secret key d is correct or not
    Returns: 1 if it is correct, 0 otherwise
    """
    y = testing_pair[0]
    S = testing_pair[1]
    S1 = long(pow(y,d,n))
    if S == S1:
        return bool(1)
    else:
        return bool(0)


def extEuclideanAlg(a, b):
    """
    Extended Euclidean algorithm
    """
    if b == 0:
        return 1, 0, a
    else:
        x, y, gcd = extEuclideanAlg(b, a % b)
        return y, x - y * (a // b), gcd


def modInvEuclid(a, n):
    """
    Computes the modular multiplicative inverse using
    the extended Euclidean algorithm
    Returns: multiplicative inverse of a modulo n
    """
    x, y, gcd = extEuclideanAlg(a, n)
    if gcd == 1:
        return x % n
    else:
        return None

############# IMPLEMENT YOUR TIMING ATTACK BELOW  ##############


def MontgomeryMul(a, b, n, n1, z):
    """
    Montgomery Multiplication
    Returns: f=a*b and er=1 if reduction is done, er=0 otherwise
    """

    # ... WRITE YOUR CODE HERE ...
    c = a * b
    d = (c * n1) % z
    e = c + n * d
    f = e / z
    if f >= n:
        f = f - n
        er = 1
    else:
        er = 0
    return f, er

## i is the ith bit of the Key from riht to left[1,64]


def MontgomeryExpErCheck(y, d, z2, n, n1, z, i):
    y1, er = MontgomeryMul(y, z2, n, n1, z)
    x1 = z
    for ii in range(64):
        x1, er = MontgomeryMul(x1, x1, n, n1, z)
        if (ii == (65 - i)):
            return er
        if testBit(d, 63 - ii):
            x1, er = MontgomeryMul(x1, y1, n, n1, z)


def perform_timing_attack(inputs, timings, testing_pair):
    """
    Timing attack
    Returns: Secret key d (64 bit integer number)
    """

    n = long(0xB935E2B84B83E9EB)  # modulus
    z  = long(pow(2,64))
    z2 = long(pow(z,2,n))
    n1 = modInvEuclid(-n, z)
    d = long(0)
    d = d ^ (1 << 63)
    er = [0]*5000
    # ... WRITE YOUR CODE HERE ...
    for i in range(62):
        d1 = d ^ (1 << (62 - i))
        d0 = d
        ##caculate the correlation when hypothesis is 0
        mean = 0.0  # caculate the mean values of inputs and er when hypothesis is 0
        MeanEr = 0.0
        er ＝ ［0］ ＊ 5000
        for j in range(5000):
            mean = mean + timings[j]
            er[j] = MontgomeryExpErCheck(inputs[j], d0, z2, n, n1, z, 63 - i)
            if (er[j] == 1):
                MeanEr += 1
        mean /= 5000.0
        MeanEr /= 5000.0
        mem = 0.0  # caculate the correlation when hypothesis is 0
        dem = 0.0
        for j in range(5000):
            mem = (timings[j] - mean) * (er[j] - MeanEr) + mem
            dem = (timings[j] - mean) * (timings[j] - mean) * (er[j] - MeanEr) * (er[j] - MeanEr)+ dem
        Cr0 = mem / math.sqrt(dem)
        ##caculate the correlation when hypothesis is 1
        MeanEr = 0
        for j in range(5000):
            er[i] = 0
        for  j in range(5000):
            er[j] = MontgomeryExpErCheck(inputs[j], d1, z2, n, n1, z, 63 - i)
            if (er[j] == 1):
                MeanEr += 1
        MeanEr /= 5000.0
        mem = 0.0  # caculate the correlation when hypothesis is 1
        dem = 0.0
        for j in range(5000):
            mem = (timings[j] - mean) * (er[j] - MeanEr) + mem
            dem = (timings[j] - mean) * (timings[j] - mean) * (er[j] - MeanEr) * (er[j] - MeanEr)+ dem
        Cr1 = mem / math.sqrt(dem)
        if (Cr0 < Cr1):
            d = d1
    # brute force last bit
    d1 = (d ^ 1)
    if testPair(testing_pair, d1, n):
       d = d1
    return d

