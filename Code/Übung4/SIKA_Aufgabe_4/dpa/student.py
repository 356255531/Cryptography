#!/usr/bin/env python
# -*- Mode: Python; tab-width: 4; coding: utf8 -*-
"""
DPA Attack on last round key of AES.

Please implement your attack in the function perform_dpa().
"""
############################## IMPORT MODULES ##################################
import numpy as np      # numeric calculations and array
import math
########################## CONSTANTS DEFINITION ################################
# Inverse S-BOX Table
Inv_SBox = np.array([
0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D
], np.uint8)

# Byte Hamming Weight Table
hamming_weight = np.array([
0,1,1,2,1,2,2,3,1,2,2,3,2,3,3,4,
1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5,
1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5,
2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,
1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5,
2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,
2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,
3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7,
1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5,
2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,
2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,
3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7,
2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,
3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7,
3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7,
4,5,5,6,5,6,6,7,5,6,6,7,6,7,7,8
], np.uint8)

####################### IMPLEMENT YOUR ATTACK BELOW ############################


def perform_dpa(ciphertexts, traces):
    ## given values:
    #ciphertexts[trace #][byte] = ciphertext        (T,B)   np.uint8
    #traces[trace #][sample] = power-consumption    (T,S)   np.uint8
    ## Sizes
    #T, S = traces.shape    #T:number of traces     #S:number of samples
    #B, K = 16, 256         #B:number of bytes      #K:number of key hypotheses

    # type conversion:
    #traces = np.float32(traces)

    ############################# PERFORM DPA ##################################

    last_round_key = np.zeros(16, np.uint8)
    # TODO: Please implement your attack here!
    T, S = traces.shape     # T:number of traces     #S:number of samples
    B, K = 16, 256          # B:number of bytes      #K:number of key hypotheses

    ##############################comprese  and caculate Tij-Tmean#############

    #compression the traces
    ComR = 50                             # Compression Rate
    DiffTraces = [None] * T
    for x in range(T):
        DiffTraces[x] = [0] * (S / ComR)
    for x in range(T):
        for y in range(S / ComR):
            for z in range(ComR):
                DiffTraces[x][y] = DiffTraces[x][y] + traces[x][y * ComR + z]
            DiffTraces[x][y] = np.float32(DiffTraces[x][y] / ComR * 1.0)
    S = S / ComR

    # Get the mean value of traces an each sample
    MeanTraces = np.zeros(S, np.float32)
    for x in range(S):
        for y in range(T):
            MeanTraces[x] = MeanTraces[x] + DiffTraces[y][x]
        MeanTraces[x] = MeanTraces[x] / T * 1.0

    # Get the power consumption - mean value
    for x in range(S):
        for y in range(T):
            DiffTraces[y][x] = DiffTraces[y][x] - MeanTraces[x]

    ###########################################################################

    # Do the 16 Bytes attack
    for i in range(B):            # make 16 times DPA for each byte
    ########################caculate the Hij-Hmean#########################
        # fulfill the M matrix with hamming weight
        DiffHW = [None] * T
        for x in range(T):
            DiffHW[x] = [0] * K
        for x in range(K):
            for y in range(T):
                DiffHW[y][x] = np.float32(hamming_weight[Inv_SBox[ciphertexts[y][i] ^ x]])

        #Get the mean value of hamming weight an each guess
        MeanHW = np.zeros(K, np.float32)
        for x in range(K):
            for y in range(T):
                MeanHW[x] = MeanHW[x] + DiffHW[y][x]
            MeanHW[x] = MeanHW[x] / T * 1.0

        # Get the hamming weight - mean value
        for x in range(K):
            for y in range(T):
                DiffHW[y][x] = DiffHW[y][x] - MeanHW[x]
        print "process end"
    ####################################################################

        # caculate the correlation cofficient
        Cr0 = 0
        Cr = 0
        Subkey = 0
        for x in range(K):
            for y in range(S):
                if (Cr > 0.5):
                    break
                mem = 0
                for z in range(T):
                    mem = mem + DiffHW[z][x] * DiffTraces[z][y]
                if (mem < 0):
                    mem = -mem
                dem1 = 0
                dem2 = 0
                for z in range(T):
                    dem1 = dem1 + DiffHW[z][x] * DiffHW[z][x]
                    dem2 = dem2 + DiffTraces[z][y] * DiffTraces[z][y]
                Cr = mem / math.sqrt(dem1 * dem2) * 1.0
                if (Cr > Cr0):
                    Cr0 = Cr
                    Subkey = x
                    print "The", i + 1, "key is", x, "Cr is", Cr
        last_round_key[i] = Subkey
    ######################### Done, OUTPUT RESULTS ############################

    return last_round_key
