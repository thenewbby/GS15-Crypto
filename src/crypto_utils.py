#!/usr/bin/env python3

import os
import re
import inspect

from math import floor, sqrt


def get_depth():
    return len(inspect.stack()) - 3

class DHParams(object):
    """docstring for ClassName"""
    def __init__(self, p, q, g):
        self.p = p
        self.q = q
        self.g = g

        

try: 
    long
except NameError: 
    long = int

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

def bytes_inv(bts, modulo):
    val = bytes2int(bts)

    return inv(val, modulo)

def inv(val, modulo):
    r, u, v = pgcde(val, modulo)

    if r == 1:
        return u%modulo
    else :
        return None

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

def fac(n):
    step = lambda x: 1 + (x<<2) - ((x>>1)<<1)
    maxq = long(floor(sqrt(n)))
    d = 1
    q = n % 2 == 0 and 2 or 3 
    while q <= maxq and n % q != 0:
        q = step(d)
        d += 1
    return q <= maxq and [q] + fac(n//q) or [n]

# def factorize(val):
#     global _known_primes
#     factor = []
#     while not is_prime(int(val)):
#         # print (val)
#         i = 0
#         while val % _known_primes[i] != 0:
#             i += 1
#             if i == len(_known_primes):
#                 _known_primes.extend([x for x in range(_known_primes[i-1] + 2, _known_primes[i-1]*10 + 1, 2) if is_prime(x)])
#         factor.append(_known_primes[i])
#         val =  int(val / _known_primes[i])

#     factor.append(int(val))
#     return factor

#=========================================================
def getPrime(nb_bytes):
    depth = get_depth()
    print("{}getPrime: Generate a {} bytes long prime".format(depth*"\t",nb_bytes))

    q = 0
    i = 0
    while True:
        i += 1
        # q = bytes2int(genKey(3, False))
        q = bytes2int(genKey(nb_bytes, False, i))
        # print (key)
        # print (is_prime(key))
        if is_prime(q):
            print ('')
            break
    return q

def genKey(nb_bytes, print_key=True, i=1):
    depth = get_depth()
    print("{}genKey: Generate a {} bytes long random number. try {}".format(depth*"\t",nb_bytes, i), end="\r")
    key = os.urandom(nb_bytes)
    # print (":".join("{:02x}".format(ord(c)) for c in rand)) # python2
    key_hex = key.hex()
    if print_key:
        print (':'.join(a+b for a,b in zip(key_hex[::2], key_hex[1::2])))
    return key

def Schnorr_prime(nb_small, nb_big):
    depth = get_depth()
    print("{}Schnorr_prime: Generate prime q".format(depth*"\t"))
    q = getPrime(nb_small)

    print("{}Schnorr_prime: Generate prime p".format(depth*"\t"))

    p = 0
    i = 1
    h = bytes2int(genKey(nb_big - nb_small, False, i))
    while True:

        p = h * q + 1
        if is_prime(p):
            print ('')
            break
        else:
            i += 1
            h = bytes2int(genKey(nb_big - nb_small, False, i))
    # bytesToString(int2bytes(p,nb_big))
    # print (is_prime(q))
    # print (is_prime(p))
    # print (1 < h < p)
    # print (p - q*h)
    return q,p

def parseKey(printed_key):
    if type(re.match('^([0-9a-f]{2}:)*[0-9a-f]{2}$', printed_key)) is not None:
        hexa = rand_hex.replace(":", "")
        return binascii.unhexlify(hexa)
    else:
        print ("Wrong key structure")
        return None

def bytesToString(byt):
    key_hex = byt.hex()
    print (':'.join(a+b for a,b in zip(key_hex[::2], key_hex[1::2])))


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

def bytes_or_bytes(bts1, bts2):
    return int2bytes(bytes2int(bts1) | bytes2int(bts2), len(bts1))

def bytes_and_bytes(bts1, bts2):
    return int2bytes(bytes2int(bts1) & bytes2int(bts2), len(bts1))

def bytes_xor_bytes(bts1, bts2):
    return int2bytes(bytes2int(bts1) ^ bytes2int(bts2), len(bts1))

def bytes_or_int(bts1, val):
    return int2bytes(bytes2int(bts1) | val, len(bts1))

def bytes_and_int(bts1, val):
    return int2bytes(bytes2int(bts1) & val, len(bts1))

def bytes_xor_int(bts1, val):
    return int2bytes(bytes2int(bts1) ^ val, len(bts1))

def bytes_times_int(bts1, val):
    return int2bytes((bytes2int(bts1)*val) % (exp_rapide(2,len(bts1)*8) + 1),len(bts1))

def bytes_plus_bytes(bts1, bts2):
    return int2bytes((bytes2int(bts1) + bytes2int(bts2)) % exp_rapide(2,len(bts1)*8),len(bts1))

def bytes_minus_bytes(bts1, bts2):
    return int2bytes((bytes2int(bts1) - bytes2int(bts2)) % exp_rapide(2,len(bts1)*8),len(bts1))
#===========================================

"""
Block cipher mode
"""

def ECB(function, file_in, file_out, chunk_size, key):
    if not isinstance(key, bytes):
        raise TypeError("key must be set to bytes")
    with open(file_in, 'rb') as f:
        s = open(file_out, 'wb')
        for chunk in iter(lambda: f.read(chunk_size), b''):
            if len(chunk) != chunk_size:
                chunk += bytes(chunk_size - len(chunk))
            s.write(function(chunk,key))
        s.close()

class CBC(object):
    """docstring for CBC"""

    @staticmethod
    def cipher(function, file_in, file_out, chunk_size, key, init_vector):
        if not isinstance(init_vector, bytes):
            raise TypeError("init_vector must be set to bytes")
        if not isinstance(key, bytes):
            raise TypeError("key must be set to bytes")
        if len(init_vector) != chunk_size:
            raise ValueError("init_vector must be the same size of the chunk size")

        with open(file_in, 'rb') as f:
            s = open(file_out, 'wb')
            last_bytes = init_vector
            for chunk in iter(lambda: f.read(chunk_size), b''):
                if len(chunk) != chunk_size:
                    chunk += bytes(chunk_size - len(chunk))
                chunk = bytes_xor_bytes(chunk, last_bytes)
                last_bytes = function(chunk,key)
                s.write(last_bytes)
            s.close()

    @staticmethod
    def decipher(function, file_in, file_out, chunk_size, key, init_vector):
        if not isinstance(init_vector, bytes):
            raise TypeError("init_vector must be set to bytes")
        if not isinstance(key, bytes):
            raise TypeError("key must be set to bytes")
        if len(init_vector) != chunk_size:
            raise ValueError("init_vector must be the same size of the chunk size")

        with open(file_in, 'rb') as f:
            s = open(file_out, 'wb')
            last_chunk = init_vector
            for chunk in iter(lambda: f.read(chunk_size), b''):
                if len(chunk) != chunk_size:
                    chunk += bytes(chunk_size - len(chunk))
                chunk_decyph = function(chunk,key)
                s.write(bytes_xor_bytes(last_chunk, chunk_decyph))
                last_chunk = chunk
            s.close()

class PCBC(object):
    """docstring for PCBC"""

    @staticmethod
    def cipher(function, file_in, file_out, chunk_size, key, init_vector):
        if not isinstance(init_vector, bytes):
            raise TypeError("init_vector must be set to bytes")
        if not isinstance(key, bytes):
            raise TypeError("key must be set to bytes")
        if len(init_vector) != chunk_size:
            raise ValueError("init_vector must be the same size of the chunk size")

        with open(file_in, 'rb') as f:
            s = open(file_out, 'wb')
            last_bytes = init_vector
            for chunk in iter(lambda: f.read(chunk_size), b''):
                if len(chunk) != chunk_size:
                    chunk += bytes(chunk_size - len(chunk))
                chunk_xor = bytes_xor_bytes(chunk, last_bytes)
                last_bytes = function(chunk_xor,key)
                s.write(last_bytes)
                last_bytes = bytes_xor_bytes(last_bytes, chunk)
            s.close()

    @staticmethod
    def decipher(function, file_in, file_out, chunk_size, key, init_vector):
        if not isinstance(init_vector, bytes):
            raise TypeError("init_vector must be set to bytes")
        if not isinstance(key, bytes):
            raise TypeError("key must be set to bytes")
        if len(init_vector) != chunk_size:
            raise ValueError("init_vector must be the same size of the chunk size")

        with open(file_in, 'rb') as f:
            s = open(file_out, 'wb')
            last_chunk = init_vector
            for chunk in iter(lambda: f.read(chunk_size), b''):
                if len(chunk) != chunk_size:
                    chunk += bytes(chunk_size - len(chunk))
                chunk_decyph = function(chunk,key)
                chunk_decyph = bytes_xor_bytes(last_chunk, chunk_decyph)
                s.write(chunk_decyph)
                last_chunk = bytes_xor_bytes(chunk, chunk_decyph)
            s.close()