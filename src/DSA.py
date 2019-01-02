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
	alice_key = diffie_hellman.DH_gen_keys(32,256) # CAN CHANGE SIZE OF q AND p

	print ("{}DSA: sign msg".format(depth*"\t"))
	sign = DSA_sign(alice_key, msg)

	print ("{}DSA: verify msg".format(depth*"\t"))
	verif = DSA_verify(sign)
	assert verif



def DSA_sign(key, msg):
	"""
	@brief      Signe le message par la methode DSA
	
	@param      key   La clé avec laquel la signature sera effectué (Classe Key)
	@param      msg   Le message
	
	@return     La signature généré (Classe DSASignature)
	"""
	depth = get_depth()
	print ("{}DSA_sign: starting function".format(depth*"\t"))
	r = s = X = 0
	h = bytes2int(hashlib.sha256(msg).digest())
	print ("{}DSA_sign: generate s&r".format(depth*"\t"))
	while s == 0:
		while r == 0:
			k = random.randint (1, key.param.q-1)
			X = pow(key.param.g, k, key.param.p)
			r = X % key.param.q
		print 
		k_inv = inv(k, key.param.q)
		if k_inv is None:
			continue

		s = (k_inv*(h + key.private_key*r)) % key.param.q
	return DSASignature(key.param, key.public_key, r, s, msg.decode())

def DSA_verify(DSA_sig):
	"""
	@brief      Vérifie la sigature du message
	
	@param      DSA_sig  La signature DSA (Classe DSASignature)
	@param      msg      Le message
	
	@return     L'état de la vérification
	"""
	depth = get_depth()
	print ("{}DSA_verify: starting function".format(depth*"\t"))

	if not (1 <= DSA_sig.r < DSA_sig.param.q and 1 <= DSA_sig.s < DSA_sig.param.q):
		return False

	h = bytes2int(hashlib.sha256(DSA_sig.msg.encode('utf-8')).digest())

	w = inv(DSA_sig.s, DSA_sig.param.q)

	u1 = (h*w) % DSA_sig.param.q
	u2 = (DSA_sig.r*w) % DSA_sig.param.q

	X = (pow(DSA_sig.param.g, u1, DSA_sig.param.p)*pow (DSA_sig.public_key, u2, DSA_sig.param.p)) % DSA_sig.param.p

	v = X % DSA_sig.param.q

	return v == DSA_sig.r


if __name__ == '__main__':
	main()