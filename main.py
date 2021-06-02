#!/usr/bin/python3
from file import File
from collections import Counter
import sys
from decimal import Decimal, getcontext

FILENAME = "index.html"
file_length = len(open(FILENAME).read())
PRECISION = 200
getcontext().prec = 200
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
            bit = int(bin_number[i : i + 8], 2)
        by.append(bit)
        i += 8

    print(by)
    data = bytes(by)
    print("data", type(data), data)
    file = File("index.html")
    file.save(data, table)


def load():
    file = File("index.html")
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
    fullencoded = encoded
    print(len(fullencoded))
    encoded_i = (0, 50)
    encoded = "0." + encoded[encoded_i[0] : encoded_i[1]]
    encoded = bin2float(encoded)
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
            # bigger = new_point(start, end, s) - Decimal(PRECISION_RANGE_BIG)
            # smaller = new_point(start, end, e) - Decimal(PRECISION_RANGE_BIG)
            bigger = new_point(start, end, s)
            smaller = new_point(start, end, e)
            if encoded >= bigger and encoded < smaller:
                decoded += key
                start1 = new_point(start, end, s)
                end1 = new_point(start, end, e)
                start, end, encoded, encoded_i = de_normalize(
                    start1, end1, encoded, numberindex=encoded_i, fullnumber=fullencoded
                )
                print(encoded_i)
                break

        i += 1
    return decoded


def get_decimals(n):
    s = str(n)
    return s[::-1].find(".")


def left_shift(bin_number, amount, position, fullnumber="", numberindex=0):
    if position == "start":
        adder = "0"
    elif position == "end":
        adder = "1"
    elif position == "number":
        numberstart, numberend = numberindex
        return fullnumber[numberstart:numberend], ""
    else:
        adder = ""
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

def de_normalize(initial_start, initial_end, initial_number, fullnumber, numberindex):
    start, end, number = (
        float2bin(initial_start),
        float2bin(initial_end),
        float2bin(initial_number),
    )
    # print("de start", start)
    amount = 0
    # for s, e in zip(list(start), list(end)):
    for i in range(len(start)):
        s, e, n = start[i], end[i], number[i]
        if s == e and s == n:
            amount += 1
        else:
            break

    # print("amount", amount)
    if amount > 0:
        numberindex = numberindex[0] + amount, numberindex[1] + amount

        start, _ = left_shift(start, amount, "start")
        end, _ = left_shift(end, amount, "end")
        number, _ = left_shift(
            number, amount, "number", fullnumber=fullnumber, numberindex=numberindex
        )
    else:
        return initial_start, initial_end, initial_number, numberindex
    PREFIX = "0."

    # print(
        # "Initial",
        # float2bin(initial_start)[0:10],
        # float2bin(initial_end)[0:10],
        # float2bin(initial_number)[0:10],
    # )
    # print("Not initial", start[0:10], end[0:10], number[0:10])

    return (
        bin2float(PREFIX + start),
        bin2float(PREFIX + end),
        bin2float(PREFIX + number),
        numberindex,
    )


if __name__ == "__main__":
    filename = "index.html"
    f = open(FILENAME, "r").read()
    table = get_table(f)
    f = f[:139]
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
