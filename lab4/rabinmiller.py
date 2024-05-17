# Author: Stanisław Olszewski

from math import gcd
import random
import sys


def fermat(num):
    for _ in range(50):
        a = random.randint(2, num - 1)
        if gcd(a, num) != 1:
            return "na pewno złożona"

        if pow(a, num - 1, num) != 1:
            return "na pewno złożona"

    return "prawdopodobnie pierwsza"


def rabinmiller(num, exponent, attempts):
    if attempts == 0:
        return "prawdopodobnie pierwsza"

    a = random.randint(2, num - 1)

    if pow(a, exponent, num) != 1:
        exponent = 0

    if not (num % 2):
        return "na pewno złożona"

    if gcd(a, num) != 1:
        return "na pewno złożona"

    b, k = quick_pow(a, num, exponent)

    if b[-1] != 1:
        return "na pewno złożona"

    if b[k] == 1:
        for j, b_j in enumerate(b):
            if j == 0:
                continue
            if b_j == 1:
                break

    j = j - 1
    if b[j] != -1:
        divider_1 = gcd(b[j] - 1, num)
        divider_2 = gcd(b[j] + 1, num)

        if divider_1 != 1 and divider_2 != 1:
            return random.choice([f"{divider_1}", f"{divider_2}"])

    return rabinmiller(num, exponent, attempts - 1)


def quick_pow(a, n, m=0):
    if m == 0:
        m = n - 1
    k = 0
    while m % 2 == 0:
        m //= 2
        k += 1

    b_0 = pow(a, m, n)
    b = [b_0]

    for j in range(k):
        b.append(pow(b[j], 2, n))

    return b, k


def main():
    with open("wejscie.txt", "r") as f:
        lines = f.readlines()

    if len(sys.argv) > 1 and sys.argv[1] == "-f":
        result = fermat(int(lines[0]))
        print("Fermat test completed")
    else:
        if len(lines) == 3:
            exponent = int(lines[1]) * int(lines[2]) - 1
        elif len(lines) == 2:
            exponent = int(lines[1])
        else:
            exponent = 0

        result = rabinmiller(int(lines[0]), exponent, 40)

        print("Rabin-Miller test completed")

    with open("wyjscie.txt", "w", encoding="utf-8") as f:
        f.write(result)


if __name__ == "__main__":
    main()
