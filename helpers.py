from decimal import Decimal, getcontext
getcontext().prec = 200

def float2bin(number, places=600):
    number = Decimal(str(number))
    rest = Decimal("0")
    result = ""
    consecutive_zeros = 0
    b = Decimal("1")
    i = 1
    while i < places:
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
