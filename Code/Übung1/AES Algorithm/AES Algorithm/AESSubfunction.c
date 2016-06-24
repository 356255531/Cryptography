//
//  AESSubfunction.c
//  
//
//  Created by Finn on 15/11/6.
//
//

#include "AESSubfunction.h"



/******************************************************************************************************************/

uchar AddRoundkey(uchar State[4][4], uchar Key[4][4])                                     //First step AddRoundKey
{
    unsigned char i,j;
    for (i=0; i<4; i++) {
        for (j=0; j<4; j++) {
            State[j][i] ^= Key[j][i];
        }
    }
    return 0;
}


/******************************************************************************************************************/

uchar SubBytes(uchar State[4][4])                                     //Second step SubBytes
{
    uchar i,j;
    for (i=0; i<4; i++) {
        for (j=0; j<4; j++) {
            State[i][j]=SBox[State[i][j]/16][ State[i][j]%16];
        }
    }
    return 0;
}


/******************************************************************************************************************/
uchar ShiftRows(uchar State[4][4])                                                        //Third step ShiftRows
{
    uchar i,j,k;
    for (i=1; i<4; i++) {
        for (j=1; j<i+1; j++) {
            uchar temp = State[i][0];
            for (k=0; k<3; i++)
                State[i][k]=State[i][k+1];
            State[i][3]=temp;
        }
    }
    return 0;
}

/******************************************************************************************************************/

uchar MixColumns(uchar State[4][4])                                                       //Forth step MixCloumns
{
    uchar i,j,k;
    uchar Temp[4][4];
    for (i=0; i<4; i++) {
        for (j=0; j<4; j++) {
            switch (MCM[i][0]) {
                case 0x01:
                    Temp[i][j] = State[0][j];
                    break;
                case 0x02:
                    Temp[i][j] = State[0][j] << 1;
                    if (State[0][j] & 0x80)
                        Temp[i][j] ^= 0x1b;
                    break;
                case 0x03:
                    Temp[i][j] = State[0][j]<<1;
                    if (State[0][j] & 0x80)
                        Temp[i][j] ^= 0x1b;
                    Temp[i][j] ^= State[0][j];
                    break;
                default:
                    break;
            }
            for (k=1; k<4; k++) {
                uchar AddFactor;
                switch (MCM[i][k]) {
                    case 0x01:
                        AddFactor = State[i][j];
                        break;
                    case 0x02:
                        AddFactor = State[i][j] << 1;
                        if (State[i][j] & 0x80)
                            AddFactor ^= 0x1b;
                        break;
                    case 0x03:
                        AddFactor = State[i][j] << 1;
                        if (State[i][j] & 0x80)
                            AddFactor ^= 0x1b;
                        AddFactor ^= State[i][j];
                        break;
                    default:
                        break;
                }
                Temp[i][j] ^= AddFactor;
            }
        }
    }
    for (i=0; i<4; i++)
        for (j=0; j<4; j++)
            State[i][j] = Temp[i][j];
    return 0;
}

/******************************************************************************************************************/
uchar KeyExpansion(uchar Key[4][4], uchar RoundNum)                                                   //KeyExpansion
{
    uint W0 = ByteToWord(Key, 0),W1 = ByteToWord(Key, 1),W2 = ByteToWord(Key, 2),W3 = ByteToWord(Key, 3);
    W0 ^= GiFunction(W3, RoundNum);
    W1 ^= W0;
    W2 ^= W1;
    W3 ^= W2;
    WordToByte(W0, Key, 0);
    WordToByte(W1, Key, 1);
    WordToByte(W2, Key, 2);
    WordToByte(W3, Key, 3);
    return 0;
}
uint ByteToWord(uchar Key[4][4],uchar k)
{
    return (Key[0][k]+Key[1][k]*0x10+Key[2][k]*0x100+Key[3][k]*0x1000);
}
uchar WordToByte(uint Word, uchar Key[4][4],uchar k)
{
    uchar i; uint WWord = Word;
    for (i=3; i >= 0; i--) {
        Key[i][k] = WWord / 0X1000;
        WWord <<= 4;
    }
    return 0;
}

uint GiFunction(uint Word, uchar RoundNum)
{
    uint WWord = Word;
    uchar B2 = WWord / 0X1000, B3 = WWord % 0x10; WWord <<=4;uchar B1 = WWord / 0x1000;WWord <<=4;uchar B0 = WWord / 0x1000;
    B3 = SBox[B3 / 0x10][ B3 % 0X10];
    B2 = SBox[B2 / 0x10][ B2 % 0X10];
    B1 = SBox[B1 / 0x10][ B1 % 0X10];
    B0 = SBox[B0 / 0x10][ B0 % 0X10];
    B0 ^= RCon[RoundNum];
    return B3 * 0X1000 + B2 * 0x100 + B1 * 0x10 + B0;
}

