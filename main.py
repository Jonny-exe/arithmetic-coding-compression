#!/usr/bin/python3
from file import File
from collections import Counter
import sys
from decimal import Decimal, getcontext

FILENAME = "my_file"
file_length = len(open(FILENAME).read())
PRECISION = file_length
getcontext().prec = PRECISION
PRECISION_RANGE = pow(10, -PRECISION)
PRECISION_RANGE_BIG = 10 * pow(10, -PRECISION)

def float2bin(number, places=PRECISION_RANGE):
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


def save(bin_number, table):
    by_i = 0
    i = 0
    by = []
    l = len(bin_number)
    print("l", l)
    rest = 8 - (l % 8)
    while i < l:
        if l < i + 8:
            bit = int(bin_number[i:l] + rest * "0", 2)
        else:
            bit = int(bin_number[i:i+8], 2)
        by.append(bit)
        i += 8

    print(by)
    data = bytes(by)
    print("data", type(data), data)
    file = File("my_file")
    file.save(data, table)

def load():
    file = File("my_file")
    data = file.load()
    return data


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
    print("OUTPUTS: ", len(outputs))
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
            s, e = r[0], r[1]
            bigger = new_point(start, end, s) - Decimal(PRECISION_RANGE_BIG)
            smaller = new_point(start, end, e) - Decimal(PRECISION_RANGE_BIG)
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

if __name__ == "__main__":
    filename = "my_file"
    f = open(FILENAME, "r").read()
    table = get_table(f)
    f = f[:1000]
    l = len(f)
    encoded = encode(f)
    print("raw: ", f)
    print("encoded: ", len(encoded), encoded)

    save(encoded, table)
    encoded = load()
    print("encoded", encoded)
    d = decode(encoded, l, f)
    print("decoded: ", d)
    if f == d:
        print("✅")
    else:
        print("❌")


