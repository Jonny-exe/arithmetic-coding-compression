import pickle
import sys
import struct


class File:
    def __init__(self, filename):
        self.filename = filename

    def load(self):
        f = open(self.filename + ".jzip", "rb")

        ftypeb = f.read(4)
        ftype = str(ftypeb, "utf-8")

        if ftype != "JZIP":
            # Raise error
            return

        f.seek(4)
        versionb = f.read(4)
        version = struct.unpack("!I", versionb)[0]

        if version != 1:
            return

        f.seek(8)
        lb = f.read(4)
        l = struct.unpack("!I", lb)[0]

        f.seek(12)
        tablelb = f.read(4)
        tablel = struct.unpack("!I", tablelb)[0]
        f.seek(16)
        tableb = f.read(tablel)
        table = pickle.loads(tableb)

        f.seek(16 + tablel)
        data = f.read()
        data = self.data_to_bin(data)
        return data, table, l

    def data_to_bin(self, data):
        result = ""
        for n in data:
            b = "{0:b}".format(n)
            b = "0" * (8 - len(b)) + b
            result += b
        return result

    def save(self, data, table, l):
        f = open(self.filename + ".jzip", "wb")

        s = "JZIP"
        f.write(bytes(s, "utf-8"))

        n = struct.pack("!I", 1)
        f.write(n)

        l = struct.pack("!I", l)
        f.write(l)

        table = pickle.dumps(table)
        print("table l:", len(table))
        tablel = struct.pack("!I", len(table))

        f.write(tablel)
        f.write(table)
        f.write(data)

        f.close()
