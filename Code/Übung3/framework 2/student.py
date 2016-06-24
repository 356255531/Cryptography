######################## IMPORT MODULES #############################

import os, sys, math, csv, time, numpy, math

###################### USEFUL ROUTINES ##############################

def testBit(val, offset):
    """
    Test whether bit at position offset is set or not
    Returns: 1 if it is set, 0 otherwise
    """
    if (val & (1 << offset))!=0:
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

def extEuclideanAlg(a, b) :
    """
    Extended Euclidean algorithm
    """
    if b == 0 :
        return 1,0,a
    else :
        x, y, gcd = extEuclideanAlg(b, a % b)
        return y, x - y * (a // b),gcd

def modInvEuclid(a,n) :
    """
    Computes the modular multiplicative inverse using
    the extended Euclidean algorithm
    Returns: multiplicative inverse of a modulo n
    """
    x,y,gcd = extEuclideanAlg(a,n)
    if gcd == 1 :
        return x % n
    else :
        return None

############# IMPLEMENT YOUR TIMING ATTACK BELOW  ##############

def MontgomeryMul(a,b,n,n1,z):
    """
    Montgomery Multiplication
    Returns: f=a*b and er=1 if reduction is done, er=0 otherwise
    """

    # ... WRITE YOUR CODE HERE ...

    return f,er

def perform_timing_attack(inputs, timings, testing_pair):
    """
    Timing attack
    Returns: Secret key d (64 bit integer number)
    """

    n = long(0xB935E2B84B83E9EB) # modulus
    z  = long(pow(2,64))
    z2 = long(pow(z,2,n))
    n1 = modInvEuclid(-n, z)

    d = long(0)

    # ... WRITE YOUR CODE HERE ...


    # brute force last bit
    d1 = (d ^ 1)
    if testPair(testing_pair, d1, n):
        d=d1

    return d

