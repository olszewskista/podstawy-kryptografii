# Test Millera-Rabina
# Data   : 14.02.2024
# (C)2024 mgr Jerzy Wałaszek
# ---------------------------

import random

G = 2 ** 64


# 64 bitowy generator pseudolosowy
# ---------------------------------
def losuj(a, b):
    w = 0
    for i in range(8):
        w <<= 8
        w |= int(random.random() * 256)
    return a + (w % (b - a))


# Funkcja mnoży a i b % n
# --------------------------
def mnoz_modulo(a, b, n):
    w, m = 0, 1
    while m < G:
        if b & m: w = (w + a) % n
        a = (a << 1) % n
        m <<= 1
    return w


# Funkcja oblicza a ** e % n
# ---------------------------
def poteguj_modulo(a, e, n):
    p, w, m = a, 1, 1
    while m < G:
        if e & m: w = mnoz_modulo(w, p, n)
        p = mnoz_modulo(p, p, n)
        m <<= 1
    return w


random.seed(None, 2)

arr = input().split(" ")
p = int(arr[0])
n = 40
# n = int(arr[1])

d, s = p - 1, 0
while not (d % 2):
    s += 1
    d //= 2
t = True
for i in range(n):
    a = losuj(2, p - 2)
    x = poteguj_modulo(a, d, p)
    if (x == 1) or (x == p - 1): continue
    j = 1
    while (j < s) and (x != p - 1):
        x = mnoz_modulo(x, x, p)
        if x == 1:
            t = False
            break
        j += 1
    if not t: break
    if x != p - 1:
        t = False
        break
if t:
    print("TAK")
else:
    print("NIE")