#!/usr/bin/env python


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