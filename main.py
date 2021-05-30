#!/usr/bin/python3

from collections import Counter
import sys


def float2bin(number, places=sys.float_info.epsilon):
    rest = 0
    result = ""
    consecutive_zeros = 0
    b = 1
    i = 1
    while b > places:
        b = 2 ** -i
        if b + rest <= number:
            result += "1"
            rest += b
        else:
            result += "0"
        i += 1
    return result


def bin2float(number):
    # TODO: make this work with not only intervals from 0 to 1
    result = 0.0
    number = number[number.find(".") + 1 :]
    for i in range(len(number)):
        c = number[i]
        if c == "1":
            result += 2 ** -(i + 1)
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

    last = 0
    l = len(f)
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
    start = 0
    end = 1
    i = 1
    ranges = table.items()
    outputs = ""
    for c in f:
        c = table[c]
        start1 = new_point(start, end, c[0])
        end1 = new_point(start, end, c[1])
        start, end, output = normalize(start1, end1)
        outputs += output

    print("outputs: ", outputs)
    print("fs: ", start)
    print("fe: ", end)
    return outputs + float2bin(start)


def reverse_table(table):
    new_table = {}
    for key in table:
        new_table[table[key]] = key
    return new_table


def decode(encoded, l, f):
    encoded = bin2float("0." + encoded)
    print("Encoded: ", encoded)
    table = get_table(f)
    start = 0
    end = 1
    i = 0
    decoded = ""

    while i < l:
        for key in table.keys():
            r = table[key]
            s, e = r[0], r[1]
            if encoded >= new_point(start, end, s) and encoded < new_point(start, end, e):
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


def left_shift(bin_number, amount, position, places=30):
    if position == "start":
        adder = "0"
    else:
        adder = "1"
    return bin_number[amount:] + adder * amount, bin_number[:amount]


def normalize(initial_start, initial_end):
    start, end = float2bin(initial_start), float2bin(initial_end)
    amount = 0
    for s, e in zip(list(start), list(end)):
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
l = len(f1)
a = encode(f1)
print("raw: ", f1)
print("encoded: ", a)
d = decode(a, l, f1)
print("decoded: ",d)
if f1 == d:
    print("✅")
else:
    print("❌")


f2 = open("test2", "r").read()
l = len(f2)
a = encode(f2)
print("raw: ", f2)
print("encoded: ", a)
print("decoded: ", decode(a, l, f2))

