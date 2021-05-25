#!/usr/bin/python3
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
f = f[:2]

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
    n = (e - s)
    r = n * p + s
    print("r: ", r)
    return r

def encode(f):
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


    print(start)
    return start

def reverse_table(table):
    new_table = {}
    for key in table:
        new_table[table[key]] = key
    return new_table



def decode(f):
    table = get_table()
    table = reverse_table(table)
    l = len(f)
    # Work on decoding

