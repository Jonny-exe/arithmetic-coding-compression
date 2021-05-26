#!/usr/bin/python3
from bigfloat import *
def bin2float (b):
    s, f = b.find('.')+1, int(b.replace('.',''), 2)
    return f/2.**(len(b)-s) if s else f


def test():
    f = open('my_file', 'wb')
    bi = [0b10001000, 0b01000100]

    by = bytes(bi)
    f.write(by)
    f.close()

    f = open('my_file', 'rb')
# fr = f.read()
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
            yield int((c & (0x80>>i)) != 0)
    f.close()

# outputs = genbits()

# Make a encoder, you'll need a batch size

f = open("my_file", "r").read()
# f = f[:2]
l = len(f)

def write():
    return

def get_table():
    table = {}
    for c in f:
        if c in table:
            table[c] += 1
        else:
            table[c] = 1

    last = 0
    l = len(f)
    for key in table:
        table[key] /= l
        table[key] += last
        temp = table[key]
        table[key] = (last, temp) # Keep a range of (start, end)
        last = temp
    return table

def new_point(s, e, p):
    # n = 
    r = (e - s) * p + s
    return r

def encode(f):
    print("encoded: ", f)
    table = get_table()
    l = len(f)
    start = 0
    end = 1
    i = 1
    ranges = table.items()
    print(len(f))
    for c in f:
        c = table[c]
        start = new_point(start, end, c[0])
        end = new_point(start, end, c[1])
        print("s:", start)


    print(start)
    return start

def reverse_table(table):
    new_table = {}
    for key in table:
        new_table[table[key]] = key
    return new_table


def new_point2(s, e, p):
    w = e - s
    return w * p + s


def decode(encoded, l):
    table = get_table()
    start = 0
    end = 1
    i = 0
    decoded = ""

    while i < l:
        for key in table.keys():
            r = table[key]
            s, e = r[0], r[1]
            print(new_point2(start, e, s))
            if encoded >= new_point2(start, end, s) and encoded < new_point2(start, end, e):
                print("HELLO")
                decoded += key
                start = new_point(start, end, s)
                end = new_point(start, end, e)
                break

        i += 1
    return decoded


def get_decimals(n):
    s = str(n)
    return s[::-1].find('.')


# Decoding theory
# Check each iteration
# -> Take number and check where it fits in the ranges
# -> then update ranges
# -> check again

a = encode(f)
print("decoded: ", decode(a, l))




# To work with long types
