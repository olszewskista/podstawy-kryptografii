from math import gcd
import random

with open('wejscie.txt', 'r') as f:
    num1 = int(f.read())

def quick_pow(a, n):
    if n == 0:
        return 1
    elif n % 2 == 1:
        return a * quick_pow(a, n - 1)
    w = quick_pow(a, n/2)
    return w * w

def fermat(n):
    for _ in range(50):
        a = random.randint(2, num1-1)
        if gcd(a, n) == 1:
            if quick_pow(a, n - 1) % n == 1:
                print('git')
                pass
            else:
                print('dupa')
                break
        else:
            print('dupa')
            break



fermat(num1)
print(quick_pow(2, 11))