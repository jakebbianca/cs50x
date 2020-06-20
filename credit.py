# function imports

from cs50 import get_int

# define relevant functions
def get_cc():
    cc = get_int(f"Please enter a credit card number: ")
    return cc


def main(cc):
    # 0
    copy = cc
    sum0 = 0
    sum1 = 0

    while copy > 0:
        dig0 = int(copy / 10) % 10
        prod = dig0 * 2
        if prod >= 10:
            ldig0 = int(prod / 10) % 10
            rdig0 = prod % 10
            prod = ldig0 + rdig0
        sum0 = sum0 + prod
        copy = int(copy / 100)

    # 1
    copy = cc

    while copy > 0:
        dig1 = copy % 10
        sum1 = sum1 + dig1
        copy = int(copy / 100)

    aggsum = sum0 + sum1

    if not aggsum % 10 == 0:
        print("INVALID")
        exit(1)

    # 2
    copy = cc
    count = 0

    while not copy == 0:
        copy = int(copy / 10)
        count += 1

    # 3
    copy = cc

    while copy >= 100:
        copy = int(copy / 10)

    ldig1 = int(copy / 10) % 10
    rdig1 = copy % 10

    if count == 15 and ldig1 == 3 and (rdig1 == 4 or rdig1 == 7):
        print("AMEX")
    elif count == 16 and ldig1 == 5 and rdig1 >= 1 and rdig1 <= 5:
        print("MASTERCARD")
    elif (count == 13 or count == 16) and ldig1 == 4:
        print("VISA")
    else:
        print("INVALID")

# call functions
cc = get_cc()

main(cc)