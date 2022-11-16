#!/usr/bin/env python3


from enum import IntEnum
from typing import Tuple


# to test commit and push
# IMPORTANT NOTE: DO NOT IMPORT THE ev3dev.ev3 MODULE IN THIS FILE


class HCResult(IntEnum):
    """
    Return codes for the Hamming Code interface
    """
    VALID = 1
    CORRECTED = 2  # whenever ANY bit has been corrected
    UNCORRECTABLE = 3


class HammingCode:
    # encoded_word = (1,0,1,0,1,1,1)
    def _init_(self, n_data=5, n_parity=4, ad_parity=1):
        self.n_data = n_data
        self.n_parity = n_parity
        self.ad_parity = ad_parity

    def decode(self, encoded_word):
        self.encoded_word = list(encoded_word)
        total = len(self.encoded_word) - self.ad_parity
        data = self.n_data
        extra = self.n_parity

        if ((pow(2, extra)) >= (data + extra + 1)):

            rcvd_word = self.encoded_word[0:total]
            print("rcvd", rcvd_word)

            OE_parity = 0

            for i, item in enumerate(self.encoded_word):
                OE_parity = OE_parity ^ item

            print(OE_parity)

            def syndrome_calc(rcvd_word, parity_transpose):
                mul = []
                for i in range(len(parity_transpose[0])):
                    sum = 0
                    for j, item in enumerate(rcvd_word):
                        sum = sum + parity_transpose[j][i] * item
                    # print(sum)
                    mul.append(sum % 2)

                return (mul)

            syndrome_calc

            def parity_matrix(total, extra, data):
                p = total
                k = extra
                l = data
                # generating n numbers in binary form

                x = [bin(i + 1)[2:].zfill(k) for i in range(p)]

                y = []
                for i, _ in enumerate(x):
                    for j, item in enumerate(x[i]):
                        y.append(item)
                # converting it from string to int
                results = list(map(int, y))
                print(results)

                # swap function to perform swap operation of lists
                def swap(parity_transpose, a, b):
                    temp = parity_transpose[a]
                    parity_transpose[a] = parity_transpose[b]
                    parity_transpose[b] = temp

                # parity_transpose[a],parity_transpose[b] = parity_transpose[b],parity_transpose[a]

                swap

                # function to create initial matrix from 1 to n numbers in binary form
                def general_matrix(n_rows, n_cols, dt):
                    m = []
                    for i in range(n_cols):
                        row_data = []
                        for j in range(n_rows):
                            row_data.append(dt[n_rows * i + j])

                        m.append(row_data)
                    return m

                general_matrix

                parity_transpose = general_matrix(k, p, results)

                lgt = len(parity_transpose)
                print("length", lgt)
                count = k
                i = 0
                while (i < lgt):
                    # print("loop",i)
                    if (((sum(parity_transpose[i]) == 1) and (parity_transpose[i][count - 1]) and 1)):
                        swap(parity_transpose, i, l + count - 1)
                        count = count - 1
                        lgt = lgt - 1
                        i = 0
                    i = i + 1

                parity = [[row[r] for row in parity_transpose] for r in range(len(parity_transpose[0]))]

                return (parity)

            parity_matrix

            par = parity_matrix(total, extra, data)
            print("parity matrix")

            print(tuple(par))
            par_transpose = [[row[r] for row in par] for r in range(len(par[0]))]
            print(par_transpose)

            synd = syndrome_calc(rcvd_word, par_transpose)
            print("synd = ", synd)
            sum_synd = sum(synd)

            # checking syndrome vector is present in parity matrix
            index = 0
            for n, item in enumerate(par_transpose):
                if ((sum_synd != 0) and (synd == item)):
                    index = n + 1

            if (index > 0):
                print("error bit position")
                print(index)
            else:
                if ((sum_synd != 0)):
                    print("not found")
                else:
                    print("No flips")

            decodeddata = rcvd_word

            if (OE_parity == 1):
                if (sum_synd == 0):
                    decodeddata = rcvd_word
                    hc = HCResult.VALID
                if (sum_synd != 0 and index > 0):
                    decodeddata[index - 1] = int(not (decodeddata[index - 1]))
                    hc = HCResult.CORRECTED
                if (sum_synd != 0 and index == 0):
                    hc = HCResult.UNCORRECTABLE
                    print(hc)
                    return (None, hc)
            if (OE_parity == 0):
                if (sum_synd == 0):
                    decodeddata = rcvd_word
                    hc = HCResult.VALID
                if (sum_synd != 0):
                    hc = HCResult.UNCORRECTABLE
                    print(hc)
                    return (None, hc)
            # table consideration
            data_dec = (tuple(decodeddata[0:5]), hc)
            print(data_dec)
            return (data_dec)
        else:
            print("enter valid number of parity bits ")
            return (0)

    decode


x = HammingCode()
x.decode((1, 1, 0, 1, 0, 1, 0, 0, 0, 0))
x.decode((1, 1, 1, 0, 0, 1, 1, 0, 0, 1))
x.decode((0, 0, 1, 1, 0, 0, 1, 0, 0, 1))
x.decode((1, 1, 0, 1, 0, 1, 0, 0, 0, 0))
x.decode((0, 0, 1, 1, 1, 0, 0, 0, 1, 0))