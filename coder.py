from helpers import float2bin, bin2float
from copy import deepcopy
from file import File
from decimal import Decimal, getcontext
from collections import Counter
class Coder:
    def __init__(self, input_string, action, table={}, l=0):
        getcontext().prec = 15
        self.l = l
        print("l: ", self.l)
        if action == "encode":
            self.table = self.get_table(input_string)
            print("table l",len(self.table))
            probability_table = self.get_table_probabilities(deepcopy(self.table))
            self.output = self.encode(input_string, probability_table)
        elif action == "decode":
            self.input_l = len(input_string)
            self.table = self.get_table_probabilities(table)
            self.output = self.decode(input_string, self.table)

    def decode(self, encoded, table):
        fullencoded = encoded
        encoded_i = (0, 600)
        encoded_number = "0." + encoded[encoded_i[0] : encoded_i[1]]
        encoded = bin2float(encoded_number)
        print("Encoded float: ", encoded)
        start = Decimal("0")
        end = Decimal("1")
        i = 0
        decoded = ""
        while i < self.l:
            if i % 5000 == 0:
                print(f"{i} / {self.l}")
            for key in table.keys():
                r = table[key]
                s, e = r[0], r[1]
                bigger = self.new_point(start, end, s)
                smaller = self.new_point(start, end, e)
                if encoded >= bigger and encoded < smaller:
                    decoded += key
                    start1 = self.new_point(start, end, s)
                    end1 = self.new_point(start, end, e)
                    start, end, encoded, encoded_i = self.de_normalize(
                        start1, end1, encoded, numberindex=encoded_i, fullnumber=fullencoded
                    )
                    break

            i += 1
        print(encoded_i)
        return decoded

    def encode(self, text, table):
        start = Decimal("0")
        end = Decimal("1")
        i = 0
        ranges = table.items()
        outputs = ""
        for c in text:
            c = table[c]
            start1 = self.new_point(start, end, c[0])
            end1 = self.new_point(start, end, c[1])
            start, end, output = self.en_normalize(start1, end1)
            outputs += output
            if i % 100000 == 0:
                print(f"{i} / {self.l}")
            if i + 10 > self.l:
                getcontext().prec = 200
            i += 1

        final = ((end - start) / Decimal("2")) + start
        print("fs: ", start)
        print("type", type(start), start)
        print("LENGTHS     : ", len(outputs), len(float2bin(start)))
        return outputs + float2bin(final, places=600)
        # return outputs


    def new_point(self, s, e, p):
        r = (e - s) * p + s
        return r


    def get_table(self, text):
        table = Counter(list(text))
        return dict(table)

    def get_table_probabilities(self, table):
        last = Decimal("0")

        for key in table:
            table[key] /= Decimal(self.l)
            table[key] += last
            temp = table[key]
            table[key] = (last, temp)  # Keep a range of (start, end)
            last = temp
        return table

    def left_shift(self, bin_number, amount, position, fullnumber="", numberindex=0):
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


    def en_normalize(self, initial_start, initial_end):
        start, end = float2bin(initial_start), float2bin(initial_end)
        amount = 0
        for i in range(len(start)):
            s, e = start[i], end[i]
            if s == e:
                amount += 1
            else:
                break

        if amount > 0:
            start, output = self.left_shift(start, amount, "start")
            end, _ = self.left_shift(end, amount, "end")
        else:
            return initial_start, initial_end, ""
        PREFIX = "0."
        return bin2float(PREFIX + start), bin2float(PREFIX + end), output

    def de_normalize(self, initial_start, initial_end, initial_number, fullnumber, numberindex):
        start, end, number = (
            float2bin(initial_start),
            float2bin(initial_end),
            float2bin(initial_number),
        )
        amount = 0
        for i in range(len(start)):
            s, e, n = start[i], end[i], number[i]
            if s == e and s == n:
                amount += 1
            else:
                break

        if amount > 0:
            if numberindex[1] + amount < self.input_l:
                numberindex = numberindex[0] + amount, numberindex[1] + amount

            start, _ = self.left_shift(start, amount, "start")
            end, _ = self.left_shift(end, amount, "end")
            number, _ = self.left_shift(
                number, amount, "number", fullnumber=fullnumber, numberindex=numberindex
            )
        else:
            return initial_start, initial_end, initial_number, numberindex
        PREFIX = "0."

        return (
            bin2float(PREFIX + start),
            bin2float(PREFIX + end),
            bin2float(PREFIX + number),
            numberindex,
        )
