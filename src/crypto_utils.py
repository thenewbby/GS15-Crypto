#!/usr/bin/env python3

import os
import re
import inspect
import random
import yaml

from math import floor, sqrt


def get_depth():
    """
    @brief      Gets the depth of the function.
    
    @return     The depth.
    """
    return len(inspect.stack()) - 3

class DHParams(object):
    """
    Classe regroupant les paramètre p, q et g
    """
    def __init__(self, p, q, g, tup):
        self.p = p
        self.q = q
        self.g = g
        self.lenth = tup

    def __repr__(self):
        return "%s(p=%r, q=%r, g=%r, lenth=%r)" % (
            self.__class__.__name__, self.p, self.q, self.g, self.tup)

    def __str__(self):
        return "(p=%r, q=%r, g=%r)" % (
            self.p, self.q, self.g)

class Key(object):
    """
    Classe regroupant les paramètres, la clé publique et privée
    """
    def __init__(self, params, Pkey, pkey):
        self.param = params
        self.public_key = Pkey
        self.private_key = pkey

    def __repr__(self):
        return "%s(param=%r, public_key=%r, private_key=%r)" % (
            self.__class__.__name__, self.param, self.public_key, self.private_key)

    def __str__ (self):
        return "Key:\n\tparam={}\n\tpublic_key={}\n\tprivate_key={}\n".format(
            self.param, self.public_key, self.private_key)
        


class DSASignature(object):
    """
    Classe regroupant les paramètres, la clé public utilisé, r et s généré par DSA
    """
    def __init__(self, params, Pkey, r, s, msgs):
        self.param = params
        self.public_key = Pkey
        self.r = r
        self.s = s
        self.msg = msgs
    def __repr__(self):
        return "%s(param=%r, public_key=%r, r=%r, s=%r, msg=%r)" % (
            self.__class__.__name__, self.param, self.public_key, self.r, self.s, self.msg)

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
    """
    pgcd(a,b): calcul du 'Plus Grand Commun Diviseur' entre les 2 nombres
    entiers a et b lien :
    http://python.jpvweb.com/python/mesrecettespython/doku.php?id=pgcd_ppcm
    
    @param      a     Une valeur
    @param      b     Une valeur
    
    @return     Le Plus Grand Commun Diviseur entre a et b
    """
    while b!=0:
        r=a%b
        a,b=b,r
    return a

def bytes_inv(bts, modulo):
    """
    @brief      Trouve l'inverse d'un bytes dans Z_modulo
    
    @param      bts     Le bytes
    @param      modulo  Le modulo
    
    @return      L'inverse du bytes dans Z_modulo
    """
    val = bytes2int(bts)

    return inv(val, modulo)

def inv(val, modulo):
    """
    @brief     Trouve l'inverse d'un entier dans Z_modulo
    
    @param      val     La valeur
    @param      modulo  Le modulo
    
    @return     L'inverse de la valeur dans Z_modulo
    """
    r, u, v = pgcde(val, modulo)

    if r == 1:
        return u%modulo
    else :
        return None

def exp_rapide(a, n):
    """
    exponentiation rapide (calcul de a^n). Version itérative
    
    @param      a     La base
    @param      n     L'exposant
    
    @return     a^n
    """
    b, m = a, n
    r = 1
    while m > 0:
        if m % 2 == 1:
            r = r * b
        b = b * b
        m = m //2
    return r 

def fac(n):
    """
    @brief      Factorisation en facteur premier
    
    @param      n     La valeur à factoriser
    
    @return     tableau des facteurs premier
    """
    step = lambda x: 1 + (x<<2) - ((x>>1)<<1)
    maxq = long(floor(sqrt(n)))
    d = 1
    q = n % 2 == 0 and 2 or 3 
    while q <= maxq and n % q != 0:
        q = step(d)
        d += 1
    return q <= maxq and [q] + fac(n//q) or [n]

#===============================================================================

def getPrime(nb_bytes):
    """
    @brief      Génère un nombre premier de nb_bytes octets

    @param      nb_bytes  Le nombre d'octet

    @return     Le nombre premier
    """
    depth = get_depth()
    print("{}getPrime: Generate a {} bytes long prime".format(depth*"\t",nb_bytes))

    q = 0
    i = 0
    while True:
        i += 1
        q = bytes2int(genKey(nb_bytes, False, i))
        if is_prime(q):
            print ('')
            break
    return q

def genKey(nb_bytes, print_key=True, i=1):
    """
    @brief      Génère une clé de nb_bytes octets
    
    @param      nb_bytes   Le nombre d'octet
    @param      print_key  afficher la clé généré
    @param      i          Le nombre d'itération
    
    @return     La clé généré en bytes
    """
    depth = get_depth()
    print("{}genKey: Generate a {} bytes long random number. try {}".format(depth*"\t",nb_bytes, i), end="\r")
    while True:
        key = os.urandom(nb_bytes)
        if bytes2int(key) != 0:
            break
    if print_key:
        key_hex = key.hex()
        print (':'.join(a+b for a,b in zip(key_hex[::2], key_hex[1::2])))
    return key

def Schnorr_group(nb_small, nb_big):
    """
    @brief      Génére un group de Schnorr
    
    @param      nb_small  Le nombre d'octes pour q
    @param      nb_big    Le nombre d'octes pour p
    
    @return     Le groupe de schorr généré dans une classe DHParams
    """
    depth = get_depth()
    print("{}Schnorr_group: Generate prime q".format(depth*"\t"))
    q = getPrime(nb_small)

    print("{}Schnorr_group: Generate prime p".format(depth*"\t"))

    p = 0
    i = 1
    # r = bytes2int(genKey(nb_big - nb_small, False, i))
    r = bytes2int(genKey(nb_big, False, i))
    while True:

        p = r * q + 1
        # p = r - ((r % (2*q)) - 1)
        if is_prime(p) and p != 1:
            print('')
            break
        else:
            i += 1
            r = bytes2int(genKey(nb_big - nb_small, False, i))
            # r = bytes2int(genKey(nb_big, False, i))

    print ("{}Schnorr_group: generate g".format(depth*"\t"))
    while True:
        h = random.randint(2, p-2)

        g = pow(h, r, p)
        if g != 1:
            break
    return DHParams(p,q,g, (nb_small, nb_big) )

def parseKey(printed_key):
    """
    @brief      Fonction permetant de parser un clé en bytes du format suivant XX:XX:XX:XX:XX
    
    @param      printed_key  La clé a parser
    
    @return     La clé en bytes
    """
    if type(re.match('^([0-9a-f]{2}:)*[0-9a-f]{2}$', printed_key)) is not None:
        hexa = rand_hex.replace(":", "")
        return binascii.unhexlify(hexa)
    else:
        print ("Wrong key structure")
        return None

def bytesToString(byt):
    """
    @brief      Affiche un bytes en str
    
    @param      byt   Le bytes à afficher
    
    """
    key_hex = byt.hex()
    print (':'.join(a+b for a,b in zip(key_hex[::2], key_hex[1::2])))

#===========================================

"""
    Convertion utils
"""

def bin2hex(binStr):
    return binStr.hex()

def hex2bin(hexStr):
    return binascii.unhexlify(hexStr)

def bytes2int(bts):
    return int.from_bytes(bts, byteorder='big')

def int2bytes(val, nb_bytes):
    return val.to_bytes(nb_bytes, byteorder='big')


#===========================================

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


#===========================================
"""
    Operation pour les Bytes
"""

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

def ECB(function, file_in, file_out, chunk_size, key, init_vector=0):
    """
    @brief      Mode ECB: chiffre/dechiffre le fichier avec la fonction de
                chiffrement et la clé passé en paramettre dans un autre fichier
    
    @param      function    La fonction de chiffrement
    @param      file_in     Le fichier d'entré
    @param      file_out    Le fichier de sortie
    @param      chunk_size  La taille du bloc
    @param      key         La clé en bytes
    
    """
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
    """Classe pour le mode CBC"""

    @staticmethod
    def cipher(function, file_in, file_out, chunk_size, key, init_vector):
        """
        @brief      Mode CBC chiffrement: chiffre le fichier avec la fonction de
                    chiffrement, la clé et le vectoeur initiale passé en
                    paramettre dans un autre fichier
        
        @param      function    La fonction de chiffrement
        @param      file_in     Le fichier d'entré
        @param      file_out    Le fichier de sortie
        @param      chunk_size  La taille du bloc
        @param      key         La clé en bytes
        @param      init_vector  Le vecteur initial
        
        """
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
        """
        @brief      Mode CBC déchiffrement: déchiffre le fichier avec la fonction de
                    chiffrement, la clé et le vectoeur initiale passé en
                    paramettre dans un autre fichier
        
        @param      function    La fonction de chiffrement
        @param      file_in     Le fichier d'entré
        @param      file_out    Le fichier de sortie
        @param      chunk_size  La taille du bloc
        @param      key         La clé en bytes
        @param      init_vector  Le vecteur initial
        
        """
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
    """Classe pour le mode PCBC"""

    @staticmethod
    def cipher(function, file_in, file_out, chunk_size, key, init_vector):
        """
        @brief      Mode PCBC chiffrement: chiffre le fichier avec la fonction
                    de chiffrement, la clé et le vectoeur initiale passé en
                    paramettre dans un autre fichier
        
        @param      function     La fonction de chiffrement
        @param      file_in      Le fichier d'entré
        @param      file_out     Le fichier de sortie
        @param      chunk_size   La taille du bloc
        @param      key          La clé en bytes
        @param      init_vector  Le vecteur initial
        
        """
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
        """
        @brief      Mode PCBC déchiffrement: déchiffre le fichier avec la
                    fonction de chiffrement, la clé et le vectoeur initiale
                    passé en paramettre dans un autre fichier
        
        @param      function     La fonction de chiffrement
        @param      file_in      Le fichier d'entré
        @param      file_out     Le fichier de sortie
        @param      chunk_size   La taille du bloc
        @param      key          La clé en bytes
        @param      init_vector  Le vecteur initial
        
        """
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

#===========================================
"""
    IO for yaml file
"""
def read_yaml(file):
    with open(file, 'r') as infile:
        return yaml.load(infile)

def write_yaml(data, file):
    with open(file, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)
