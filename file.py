import pickle
import struct

class File:
    def __init__(self, filename):
        self.filename = filename

    def load(self):
        f = open(self.filename + ".jzip", "rb")

        ftypeb = f.read(4)
        print("typeb", ftypeb )
        ftype = str(ftypeb , "utf-8")
        print("type", ftype)

        if ftype != "JZIP":
            # Raise error
            return

        f.seek(4)
        versionb = f.read(4)
        print("versionb", versionb)
        version = struct.unpack("!I", versionb)[0]
        print("version", version)

        if version != 1:
            return

        f.seek(8)
        tablelb = f.read(4)
        print("tlb", tablelb)
        tablel = struct.unpack("!I", tablelb)[0]
        print("tl", tablel)
        f.seek(12)
        tableb = f.read(tablel)
        print("tableb", tableb)
        table = pickle.loads(tableb)
        print("table", table)

        f.seek(12 + tablel)
        data = f.read()
        data = self.data_to_bin(data)
        print("data", data)
        return data

    def data_to_bin(self, data):
        result = ""
        for n in data:
            b = "{0:b}".format(n)
            print(type(b))
            b = "0" * (8 - len(b)) + b
            result += b
        return result


    def save(self, data, table):
        f = open(self.filename + ".jzip", "wb")

        s = "JZIP"
        f.write(bytes(s, "utf-8"))

        n = struct.pack("!I", 1)
        print("n", n)
        f.write(n)

        table = pickle.dumps(table)
        l = struct.pack("!I", len(table))
        print("l", l)
        f.write(l)
        f.write(table)
        f.write(data)

        f.close()

