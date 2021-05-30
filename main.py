#!/usr/bin/python3
from collections import Counter
import sys
from decimal import Decimal, getcontext

getcontext().prec = 200


def float2bin(number, places=1e-200):
    number = Decimal(str(number))
    rest = Decimal("0")
    result = ""
    consecutive_zeros = 0
    b = Decimal("1")
    i = 1
    while b > places:
        b = Decimal(str(2)) ** Decimal(str(-i))
        if b + rest <= number:
            result += "1"
            rest += b
        else:
            result += "0"
        i += 1
    return result


def bin2float(number):
    # TODO: make this work with not only intervals from 0 to 1
    result = Decimal("0")
    number = number[number.find(".") + 1 :]
    for i in range(len(number)):
        c = number[i]
        if c == "1":
            result += Decimal(str(2)) ** Decimal(str(-(i + 1)))
    return result


def genbits():
    # This returns each bit individually from all the bytes of the file
    for c in fr:
        # Go into each bytes
        for i in range(8):
            # (0x80 >> i) Simulate a byte that in binary is 0b1, 0b01, 0b001 where
            # the 1 is each time in one spot

            # (c & (0x80>>i)) != 0 This checks c has a 1 in the spot where 0x80>>i has
            # a one. If it has a one in that spot it will return the number, which has a
            # one, therefore, is not 0. Then you convert the bool into an int. with 0 = false and
            # true = 1
            yield int((c & (0x80 >> i)) != 0)
    f.close()


# outputs = genbits()


def write(bin_number):
    for c in bin_number:
        # TODO
        pritn()
    b = bytes(a)

    f = open("test.jz", "wb")
    f.write(b)


def get_table(f):
    table = Counter(list(f))

    last = Decimal("0")
    l = Decimal(str(len(f)))
    for key in table:
        table[key] /= l
        table[key] += last
        temp = table[key]
        table[key] = (last, temp)  # Keep a range of (start, end)
        last = temp
    return table


def new_point(s, e, p):
    r = (e - s) * p + s
    return r


def encode(f):
    table = get_table(f)
    print("Alphabet size: ", len(table))
    l = len(f)
    start = Decimal("0")
    end = Decimal("1")
    i = 1
    ranges = table.items()
    outputs = ""
    for c in f:
        c = table[c]
        start1 = new_point(start, end, c[0])
        end1 = new_point(start, end, c[1])
        start, end, output = normalize(start1, end1)
        outputs += output

    print("fs: ", start)
    return outputs + float2bin(start)


def decode(encoded, l, f):
    encoded = bin2float("0." + encoded)
    print("Encoded: ", encoded)
    table = get_table(f)
    start = Decimal("0")
    end = Decimal("1")
    i = 0
    decoded = ""

    print(table.keys())
    while i < l:
        for key in table.keys():
            r = table[key]
            print("ranges: ", key, r)
            s, e = r[0], r[1]
            print("NEWPÔINT: ", f"[{new_point(start, end, s)},{new_point(start, end, e)})")
            bigger = new_point(start, end, s) - Decimal("5e-200")
            smaller = new_point(start, end, e) - Decimal("5e-200")
            if encoded >= bigger and encoded < smaller:
                decoded += key
                start1 = new_point(start, end, s)
                end1 = new_point(start, end, e)
                start, end = start1, end1
                break

        i += 1
    return decoded


def get_decimals(n):
    s = str(n)
    return s[::-1].find(".")


def left_shift(bin_number, amount, position, places=30):
    if position == "start":
        adder = "0"
    else:
        adder = "1"
    return bin_number[amount:] + adder * amount, bin_number[:amount]


def normalize(initial_start, initial_end):
    start, end = float2bin(initial_start), float2bin(initial_end)
    amount = 0
    # for s, e in zip(list(start), list(end)):
    for i in range(len(start)):
        s, e = start[i], end[i]
        if s == e:
            amount += 1
        else:
            break

    if amount > 0:
        start, output = left_shift(start, amount, "start")
        end, _ = left_shift(end, amount, "end")
    else:
        return initial_start, initial_end, ""
    PREFIX = "0."
    return bin2float(PREFIX + start), bin2float(PREFIX + end), output


f1 = open("my_file", "r").read()
f1 = f1[:1000]
l = len(f1)
a = encode(f1)
print("raw: ", f1)
print("encoded: ", a)
d = decode(a, l, f1)
print("decoded: ", d)
if f1 == d:
    print("✅")
else:
    print("❌")


"""
Decoding theory
Check each iteration
-- Take number and check where it fits in the ranges
-- then update ranges
-- check again
"""


"""
Normalize

-- float2bin (bin type string)
-- check and shift (in type string)

"""
