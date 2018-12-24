#!/usr/bin/env python3

from crypto_utils import *
import diffie_hellman
import hashlib
import random
import inspect




def main():
	depth = get_depth()
	print ("{}DSA: starting function".format(depth*"\t"))

	msg = b"fnvopnpfaejiddffnjnjqmdknm"

	print ("{}DSA: generate diffie_hellman keys".format(depth*"\t"))
	# DH_param, public_key, private_key = diffie_hellman.DH_gen_keys(32,256) # CAN CHANGE SIZE OF q AND p
	alice_key = diffie_hellman.DH_gen_keys(32,256) # CAN CHANGE SIZE OF q AND p

	print ("{}DSA: sign msg".format(depth*"\t"))
	sign = DSA_sign(alice_key, msg)

	print ("{}DSA: verify msg".format(depth*"\t"))
	verif = DSA_verify(sign, msg)
	# print (verif)
	assert verif



def DSA_sign(key, msg):
	depth = get_depth()
	print ("{}DSA_sign: starting function".format(depth*"\t"))
	r = s = X = 0
	# h = HASH
	h = bytes2int(hashlib.sha256(msg).digest())
	# print ("hash : {}".format(h))
	print ("{}DSA_sign: generate s&r".format(depth*"\t"))
	while s == 0:
		while r == 0:
			k = random.randint (1, key.param.q-1)
			X = pow(key.param.g, k, key.param.p)
			r = X % key.param.q
			# if r == 0:
			# 	print("YOLO", end='\r')
			# print("r : {}".format(r))
		print 
		k_inv = inv(k, key.param.q)
		if k_inv is None:
			# print("NO invert")
			continue
		# print ("k_inv : {}".format(k_inv))

		s = (k_inv*(h + key.private_key*r)) % key.param.q
		# if s == 0:
		# 	print("SOLO {} {} {} {}".format(k_inv, private_key, r, DH_param.q), end='\r')

		# print ("s : {}".format(s))

	# print ("r : {}".format(r))
	# print ("s : {}".format(s))

	return DSASignature(key.param, key.public_key, r, s)

def DSA_verify(DSA_sig, msg):
	depth = get_depth()
	print ("{}DSA_verify: starting function".format(depth*"\t"))

	# if 1 < DSA_sig.r < DH_param.q-1:
	# 	print ("r inside")

	# if 1 < DSA_sig.s < DH_param.q-1:
	# 	print ("s inside")

	if not (1 <= DSA_sig.r < DSA_sig.param.q and 1 <= DSA_sig.s < DSA_sig.param.q):
		return False

	h = bytes2int(hashlib.sha256(msg).digest())
	# print ("hash : {}".format(h))

	w = inv(DSA_sig.s, DSA_sig.param.q)

	u1 = (h*w) % DSA_sig.param.q
	u2 = (DSA_sig.r*w) % DSA_sig.param.q

	X = (pow(DSA_sig.param.g, u1, DSA_sig.param.p)*pow (DSA_sig.public_key, u2, DSA_sig.param.p)) % DSA_sig.param.p

	v = X % DSA_sig.param.q

	# print ("v : {}".format(v))
	# print ("r : {}".format(DSA_sig.r))
	# print ()

	# print ("g^q : {}".format(pow(DSA_sig.param.g, DSA_sig.param.q, DSA_sig.param.p)))
	# # Sr = (DH_param.p-1)//DH_param.q
	# # print ("g^r : {}".format(pow(DH_param.g, Sr, DH_param.p)))
	# print ("g^p : {}".format(pow(DSA_sig.param.g, DSA_sig.param.p-1, DSA_sig.param.p)))

	return v == DSA_sig.r


# used param(p,q,g) pub_key, priv_key
if __name__ == '__main__':
	main()