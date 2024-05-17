#Piotr Stróżyk
# 278795
# 16.05.2024

import sys
import random

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# def pow(base, exponent, modulus):
#     result = 1
#     base %= modulus
#     while exponent > 0:
#         if exponent % 2 == 1:
#             result = (result * base) % modulus
#         exponent = exponent >> 1
#         base = (base * base) % modulus
#     return result

def read_numbers():
    with open("wejscie.txt", "r") as input:
        lines = input.readlines()
        number1 = int(lines[0]) if len(lines) > 0 else None
        number2 = int(lines[1]) if len(lines) > 1 else None
        number3 = int(lines[2]) if len(lines) > 2 else None
    return number1, number2, number3

def write_result(result):
    with open("wyjscie.txt", "w") as output:
        output.write(str(result))

def fermat(number1):
    a = random.randint(2, number1-1)
    m = number1 - 1
    x = pow(a, m, number1)
    if x != 1:
        return "prawdopodobnie zlozona"
    else:
        return "brak pewnosci, dla a =" + str(a)
    
def rabinMiller(number1, number2, number3):
    if number3:
        number2 = (number2*number3)-1
    m = number2 if number2 else number1 - 1
    k = 0
    while m % 2 == 0:
        k += 1
        m //= 2
    for i in range(0, 40):
        a = random.randint(2, number1-1)
        if gcd(a, number1) != 1:
            divisor = gcd(a, number1)
            return divisor if divisor != number1 else "prawdopodobnie pierwsza"
        x = pow(a, m, number1)
        if x == 1 or x == number1-1:
            continue
        for j in range(0, k):
            before = x
            x = pow(x, 2, number1)
            if x == 1:
                ret = gcd(before-1, number1)
                if ret != 1 and ret != number1:
                    return ret
        if x != 1:
            return "na pewno zlozona"
    return "prawdopodobnie pierwsza"

def main():
    number1, number2, number3 = read_numbers()
    if len(sys.argv)>1:
        if sys.argv[1] == "-f":
            result = fermat(number1)
        else:
            print("Incorrect Parameter")
    else:
        result = rabinMiller(number1, number2, number3)
    write_result(result)

if __name__ == "__main__":
    main()