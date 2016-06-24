import os, sys, math

def bin64(x):
    """
    Return binary string representation of x (fixed size 64)
    """
    count=64
    return "".join(map(lambda y:str((x>>y)&1), range(count-1, -1, -1)))

def hex64(x):
    """
    Return hex string representation of x (fixed size 64)
    """
    count=64
    return ["%02X" % (x >> count-(8*(i+1)) & 0x00000000000000FF ) \
        for i in range(count/8) ]

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
    Computes the modular multiplicative inverse using the
    extended Euclidean algorithm
    Returns: multiplicative inverse of a modulo n
    """
    x,y,gcd = extEuclideanAlg(a,n)
    if gcd == 1 :
        return x % n
    else :
        return None

def MontgomeryMul(a,b,n,n1,z):
    """
    Montgomery Multiplication
    """
    # WRITE YOUR CODE HERE
    c = a*b
    d = (c * n1) % z
    e = c+n*d
    f = e / z
    if f>= n:
        f = f-n
    return f

def MontgomeryExp(y,d,z2,n,n1,z):
    """
    Left-to-right Square & Multiply using Montgomery Multiplication
    """
    y1 = MontgomeryMul(y,z2,n,n1,z)
    x1 = z
    for i in range(64):
        x1 = MontgomeryMul(x1,x1,n,n1,z)
        if ((d>>(63-i))&1):
            x1 = MontgomeryMul(x1,y1,n,n1,z)
    x = MontgomeryMul(x1,1,n,n1,z)
    return x

def RSA_Decrypt(y,d,n):
    # WRITE YOUR CODE HEREs
    z  = pow(2,64)
    z2 = pow(z,2) % n
    n1 = modInvEuclid(-n,z)
    D  = MontgomeryExp(y,d,z2,n,n1,z)
    return D

