################################################################################
#                Skeleton script for a DFA attack against AES                  #
################################################################################
#                                                                              #
# Sichere Implementierung kryptographischer Verfahren WS 2013-2014             #
# Technische Universitaet Muenchen                                             #
# Institute for Security in Information Technology                             #
# Prof. Dr.-Ing. Georg Sigl                                                    #
#                                                                              #
################################################################################

############################## IMPORT MODULES ##################################

import os, sys, math, csv, time
from numpy import *

################################# AES Routines #################################

# AES Inverted S-box
rsbox = [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3,
         0x9e, 0x81, 0xf3, 0xd7, 0xfb , 0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f,
         0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb , 0x54,
         0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b,
         0x42, 0xfa, 0xc3, 0x4e , 0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24,
         0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25 , 0x72, 0xf8,
         0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d,
         0x65, 0xb6, 0x92 , 0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda,
         0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84 , 0x90, 0xd8, 0xab,
         0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3,
         0x45, 0x06 , 0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1,
         0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b , 0x3a, 0x91, 0x11, 0x41,
         0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6,
         0x73 , 0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9,
         0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e , 0x47, 0xf1, 0x1a, 0x71, 0x1d,
         0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b ,
         0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0,
         0xfe, 0x78, 0xcd, 0x5a, 0xf4 , 0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07,
         0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f , 0x60,
         0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f,
         0x93, 0xc9, 0x9c, 0xef , 0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5,
         0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61 , 0x17, 0x2b,
         0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55,
         0x21, 0x0c, 0x7d]

def invSubBytes(in_val):
    out_val = rsbox[in_val]

    return out_val

def gfmul256(a, b):
    p = 0
    while b:
        if b & 1: p ^= a
        a <<= 1
        if a & 0x100:
            a ^= 0x1b
        b >>= 1
    return p & 0xff


def mixColumn(in_column):

    v0, v1, v2, v3 = in_column

    out_column = [ gfmul256(v0, 2) ^ gfmul256(v1, 3) ^ v2 ^ v3,
                   v0 ^ gfmul256(v1, 2) ^ gfmul256(v2, 3) ^ v3,
                   v0 ^ v1 ^ gfmul256(v2, 2) ^ gfmul256(v3, 3),
                   gfmul256(v0, 3) ^ v1 ^ v2 ^ gfmul256(v3, 2)]

    return out_column

####################### IMPLEMENT YOUR DFA ATTACK BELOW  #######################


def FindByte(NumColumn, NumEquation):
    if (NumColumn == 0):
        if (NumEquation == 1):
            return 7, 13
        if (NumEquation == 2):
            return 0, 10
        if (NumEquation == 3):
            return 13, 10
    if (NumColumn == 1):
        if (NumEquation == 1):
            return 14, 4
        if (NumEquation == 2):
            return 11, 1
        if (NumEquation == 3):
            return 4, 1

    if (NumColumn == 2):
        if (NumEquation == 1):
            return 5, 8
        if (NumEquation == 2):
            return 2, 15
        if (NumEquation == 3):
            return 8, 15

    if (NumColumn == 3):
        if (NumEquation == 1):
            return 12, 6
        if (NumEquation == 2):
            return 9, 3
        if (NumEquation == 3):
            return 6, 3


def EquationJudge(NumEquation, FA1, FA2):
    if (NumEquation == 1):
        if (FA1 == gfmul256(FA2, 3)):
            return True
        else:
            return False

    if (NumEquation == 2):
        if (FA1 == gfmul256(FA2, 2)):
            return True
        else:
            return False

    if (NumEquation == 3):
        if (FA1 == FA2):
            return True
        else:
            return False


def FindKey(NumColumn, NumEquation,correct_ciphertexts,faulty_ciphertexts):
    Key = zeros(6,uint8)
    NumKey = 0
    for FirstKeyHy in range(256):
        for SecondKeyHy in range(256):
        ## Get the number of corresbonding two bytes of correct_ciphertext and faulty_ciphertext
            m, n = FindByte(NumColumn,NumEquation)
            CorrectByte11, CorrectByte12 = correct_ciphertexts[0][m], correct_ciphertexts[0][n]
            CorrectByte21, CorrectByte22 = correct_ciphertexts[1][m], correct_ciphertexts[1][n]
            FaultyByte11, FaultyByte12 = faulty_ciphertexts[0][m], faulty_ciphertexts[0][n]
            FaultyByte21, FaultyByte22 = faulty_ciphertexts[1][m], faulty_ciphertexts[1][n]
            ## Do the inverse transformation and get the two bytes in the 9th Round
            CorrectByte11 = CorrectByte11 ^ FirstKeyHy
            CorrectByte12 = CorrectByte12 ^ SecondKeyHy
            CorrectByte21 = CorrectByte21 ^ FirstKeyHy
            CorrectByte22 = CorrectByte22 ^ SecondKeyHy

            FaultyByte11 = FaultyByte11 ^ FirstKeyHy
            FaultyByte12 = FaultyByte12 ^ SecondKeyHy
            FaultyByte21 = FaultyByte21 ^ FirstKeyHy
            FaultyByte22 = FaultyByte22 ^ SecondKeyHy

            CorrectByte11 = invSubBytes(CorrectByte11)
            CorrectByte12 = invSubBytes(CorrectByte12)
            CorrectByte21 = invSubBytes(CorrectByte21)
            CorrectByte22 = invSubBytes(CorrectByte22)

            FaultyByte11 = invSubBytes(FaultyByte11)
            FaultyByte12 = invSubBytes(FaultyByte12)
            FaultyByte21 = invSubBytes(FaultyByte21)
            FaultyByte22 = invSubBytes(FaultyByte22)

            ## Do the xor and find out the Faulty
            FA1 = CorrectByte11 ^ FaultyByte11
            FA2 = CorrectByte12 ^ FaultyByte12
            FA3 = CorrectByte21 ^ FaultyByte21
            FA4 = CorrectByte22 ^ FaultyByte22


            ## Check if the equation ist satisfied
            if EquationJudge(NumEquation, FA1, FA2) & EquationJudge(NumEquation, FA3, FA4):
                Key[NumKey], Key[NumKey + 1] = FirstKeyHy, SecondKeyHy
                NumKey = NumKey + 2
    return Key, NumKey / 2


def perform_dfa(correct_ciphertexts, faulty_ciphertexts):
    key = zeros(16)

    for NumColumn in range(4):  # The Number of column in 9th Round
        PossKey1, NumKey1 = FindKey(NumColumn,1,correct_ciphertexts,faulty_ciphertexts)
        PossKey2, NumKey2 = FindKey(NumColumn,2,correct_ciphertexts,faulty_ciphertexts)
        PossKey3, NumKey3 = FindKey(NumColumn,3,correct_ciphertexts,faulty_ciphertexts)
        for i in range(NumKey3):
            for j in range(NumKey1):
                if PossKey3[2 * i] == PossKey1[2 * j + 1]:
                    m, n = FindByte(NumColumn,1)
                    key[m], key[n] = PossKey1[2 * j], PossKey1[2 * j + 1]
            for j in range(NumKey2):
                if PossKey3[2 * i + 1] == PossKey2[2 * j + 1]:
                    m, n = FindByte(NumColumn,2)
                    key[m], key[n] = PossKey2[2 * j], PossKey2[2 * j + 1]  # ...
    print key
    return key

