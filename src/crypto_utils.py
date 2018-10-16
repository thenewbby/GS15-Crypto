#!/usr/bin/env python

import os
import re


"""
    Test de miller-rabin
    lien : https://rosettacode.org/wiki/Miller%E2%80%93Rabin_primality_test#Python
"""

def _try_composite(a, d, n, s):
    if pow(a, d, n) == 1:
        return False
    for i in range(s):
        if pow(a, 2**i * d, n) == n-1:
            return False
    return True # n  is definitely composite
 
def is_prime(n, _precision_for_huge_n=16):
    if n in _known_primes or n in (0, 1):
        return True
    if any((n % p) == 0 for p in _known_primes):
        return False
    d, s = n - 1, 0
    while not d % 2:
        d, s = d >> 1, s + 1
    # Returns exact according to http://primes.utm.edu/prove/prove2_3.html
    if n < 1373653: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3))
    if n < 25326001: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5))
    if n < 118670087467: 
        if n == 3215031751: 
            return False
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7))
    if n < 2152302898747: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11))
    if n < 3474749660383: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13))
    if n < 341550071728321: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13, 17))
    # otherwise
    return not any(_try_composite(a, d, n, s) 
                   for a in _known_primes[:_precision_for_huge_n])
 
_known_primes = [2, 3]
_known_primes += [x for x in range(5, 1000, 2) if is_prime(x)]

#=========================================================

def pgcde(a, b):
    """ pgcd étendu avec les 2 coefficients de bézout u et v
        Entrée : a, b entiers
        Sorties : r = pgcd(a,b) et u, v entiers tels que a*u + b*v = r

        SI r = 1 (pgcd(a,b) = 1):
            - u est l'inverse modulaire de a mod(b) 
            - v est l'inverse modulaire de b mod(a)

    lien : http://python.jpvweb.com/python/mesrecettespython/doku.php?id=pgcd_ppcm
    """
    r, u, v = a, 1, 0
    rp, up, vp = b, 0, 1
    while rp != 0:
        q = r//rp
        rs, us, vs = r, u, v
        r, u, v = rp, up, vp
        rp, up, vp = (rs - q*rp), (us - q*up), (vs - q*vp)
    return (r, u, v)

def pgcd(a,b):
    """pgcd(a,b): calcul du 'Plus Grand Commun Diviseur' entre les 2 nombres entiers a et b
        lien : http://python.jpvweb.com/python/mesrecettespython/doku.php?id=pgcd_ppcm
    """
    while b!=0:
        r=a%b
        a,b=b,r
    return a

def exp_rapide(a, n):
    """exponentiation rapide (calcul de a^n). Version itérative"""
    b, m = a, n
    r = 1
    while m > 0:
        if m % 2 == 1:
            r = r * b
        b = b * b
        m = m //2
    return r 

def factorize(val):
    global _known_primes
    factor = []
    while not is_prime(int(val)):
        print (val)
        i = 0
        while val % _known_primes[i] != 0:
            i += 1
            if i == len(_known_primes):
                _known_primes.extend([x for x in range(_known_primes[i-1] + 2, _known_primes[i-1]*10 + 1, 2) if is_prime(x)])
        factor.append(_known_primes[i])
        val =  int(val / _known_primes[i])

    factor.append(int(val))
    return factor

#=========================================================


def genKey(nb_bytes):
    key = os.urandom(nb_bytes)
    # print (":".join("{:02x}".format(ord(c)) for c in rand)) # python2
    key_hex = key.hex()
    print (':'.join(a+b for a,b in zip(key_hex[::2], key_hex[1::2])))
    return key

def parseKey(printed_key):
    if type(re.match('^([0-9a-f]{2}:)*[0-9a-f]{2}$', printed_key)) is not None:
        hexa = rand_hex.replace(":", "")
        return binascii.unhexlify(hexa)
    else:
        print ("Wrong key structure")
        return None

def bin2hex(binStr):
    return binStr.hex()

def hex2bin(hexStr):
    return binascii.unhexlify(hexStr)

def bytes2int(bts):
    return int.from_bytes(bts, byteorder='big')

def int2bytes(val, nb_bytes):
    return val.to_bytes(nb_bytes, byteorder='big')

"""
rotation binaire:
lien :  X http://python.jpvweb.com/python/mesrecettespython/doku.php?id=binaire
        X https://gist.github.com/cincodenada/6557582
        https://www.geeksforgeeks.org/rotate-bits-of-an-integer/
"""

rol = lambda val, r_bits, max_bits: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))
 
# Rotate right: 0b1001 --> 0b1100
ror = lambda val, r_bits, max_bits: \
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))

def bytes_rol(bts, r_bits):
    temp = bytes2int(bts)
    temp = rol(temp, r_bits , len(bts)*8)
    return int2bytes(temp, len(bts))

def bytes_ror(bts, r_bits):
    temp = bytes2int(bts)
    temp = ror(temp, r_bits , len(bts)*8)
    return int2bytes(temp, len(bts))

def bytes_or(bts1, bts2):
    return int2bytes(bytes2int(bts1) | bytes2int(bts2), len(bts1))

def bytes_and(bts1, bts2):
    return int2bytes(bytes2int(bts1) & bytes2int(bts2), len(bts1))

def bytes_or(bts1, bts2):
    return int2bytes(bytes2int(bts1) ^ bytes2int(bts2), len(bts1))

