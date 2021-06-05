#!/usr/bin/python3
from file import File
from coder import Coder

FILENAME = "test"

def save(bin_number, table, length):
    by_i = 0
    i = 0
    by = []
    l = len(bin_number)
    rest = 8 - (l % 8)
    while i < l:
        if l < i + 8:
            bit = int(bin_number[i:l] + rest * "0", 2)
        else:
            bit = int(bin_number[i : i + 8], 2)
        by.append(bit)
        i += 8

    data = bytes(by)
    file = File(FILENAME)
    file.save(data, table, length)


def load():
    file = File(FILENAME)
    data, table, l = file.load()
    return data, table, l

if __name__ == "__main__":
    input_string = open(FILENAME).read()
    coder = Coder(input_string, "encode", l=len(input_string))
    output, l, table = coder.output, coder.l, coder.table
    print("L output", len(output))
    save(output, table, l)

    data, table, l = load()
    coder = Coder(data, "decode", table=table, l=l)
    if input_string == coder.output:
        print("✅")
    else:
        print("output", coder.output)
        print("❌")
    print("COMPARE")
    print(input_string[-50:])
    print(coder.output[-50:])

