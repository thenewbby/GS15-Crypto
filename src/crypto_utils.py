#!/usr/bin/env python

import os
import re

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


"""
rotation binaire:
lien :  http://python.jpvweb.com/python/mesrecettespython/doku.php?id=binaire
        https://gist.github.com/cincodenada/6557582
        https://www.geeksforgeeks.org/rotate-bits-of-an-integer/
"""