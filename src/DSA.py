#!/usr/bin/env python3

from crypto_utils import *
import diffie_hellman
import hashlib
import random
import inspect

class DSASignature(object):
	"""docstring for DSASignature"""
	def __init__(self, r, s):
		self.r = r
		self.s = s


def main():
	depth = get_depth()
	print ("{}DSA: starting function".format(depth*"\t"))

	msg = b"suprise mother fucking mother fucker. Hodbsdzlcdbjzmqdbldjvbldjbvaljdvllagdclkjn"
	# q,p = Schnorr_prime(32,256)
	# print (int2bytes(q, 32))
	# bytesToString(int2bytes(q, 32))

	# print ()

	# bytesToString(int2bytes(p, 256))
	print ("{}DSA: generate diffie_hellman keys".format(depth*"\t"))
	DH_param, public_key, private_key = diffie_hellman.DH_gen_keys()
	print ("{}DSA: sign msg".format(depth*"\t"))
	sign = DSA_sign(DH_param, private_key, msg)

	print ("{}DSA: verify msg".format(depth*"\t"))
	verif = DSA_verify(DH_param, public_key, sign, msg)
	print (verif)


def DSA_sign(DH_param, private_key, msg):
	depth = get_depth()
	print ("{}DSA_sign: starting function".format(depth*"\t"))
	r = s = X = 0
	# h = HASH
	h = bytes2int(hashlib.sha256(msg).digest())
	# print ("hash : {}".format(h))
	print ("{}DSA_sign: generate s&r".format(depth*"\t"))
	while s == 0:
		while r == 0:
			k = random.randint (1, DH_param.p-1)
			X = pow(DH_param.g, k, DH_param.p)
			r = X % DH_param.q
			# print("r : {}".format(r))

		k_inv = inv(k, DH_param.q)
		# print ("k_inv : {}".format(k_inv))

		s = (k_inv*(h + private_key*r)) % DH_param.q

	# print ("r : {}".format(r))
	# print ("s : {}".format(s))

	return DSASignature(r,s)

def DSA_verify(DH_param, public_key, DSA_sig, msg):
	depth = get_depth()
	print ("{}DSA_verify: starting function".format(depth*"\t"))

	# if 1 < DSA_sig.r < DH_param.q-1:
	# 	print ("r inside")

	# if 1 < DSA_sig.s < DH_param.q-1:
	# 	print ("s inside")

	if not (1 < DSA_sig.r < DH_param.q-1 and 1 < DSA_sig.s < DH_param.q-1):
		return False

	h = bytes2int(hashlib.sha256(msg).digest())
	# print ("hash : {}".format(h))

	w = inv(DSA_sig.s, DH_param.q)

	u1 = (h*w) % DH_param.q
	u2 = (DSA_sig.r*w) % DH_param.q

	X = (pow(DH_param.g, u1, DH_param.p)*pow (public_key, u2, DH_param.p)) % DH_param.p

	v = X % DH_param.q

	print ("v : {}".format(v))
	print ("r : {}".format(DSA_sig.r))


	if v == DSA_sig.r:
		return True
	else:
		return False


# used param(p,q,g) pub_key, priv_key
if __name__ == '__main__':
	main()