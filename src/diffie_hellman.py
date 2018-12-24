#!/usr/bin/env python3

from crypto_utils import *
import random
import inspect
import sys

# https://www.baylon-industries.com/news/?p=1430
# https://crypto.stackexchange.com/questions/9006/how-to-find-generator-g-in-a-cyclic-group
ERASE_LINE = '\x1b[2K'
def main ():

	# DH_param, A, a = DH_gen_keys()
	alice_key = DH_gen_keys()
	# print (DH_param)
	# print (A)
	# print (a)
	# print()
	com_key_b, B, b =  DH_comm_estab_Bob(alice_key.param, alice_key.public_key)
	# print (com_key_b)
	# print (B)
	# print (b)
	# print()
	com_key_a = DH_comm_estab_Alice(alice_key.param, B, alice_key.private_key)

	assert com_key_b == com_key_a
	A_hex = int2bytes(com_key_a, 128)
	print (A_hex)
	


def DH_gen_keys(lenth_q=64, lenth_p=128):
	depth = get_depth()
	print ("{}DH_gen_keys: function starting".format(depth*"\t"))
	DH_param = Schnorr_group(lenth_q, lenth_p)
	
	print ("{}DH_gen_keys: generate private key".format(depth*"\t"))
	private_key = random.randint (1, DH_param.q)

	print ("{}DH_gen_keys: generate public key".format(depth*"\t"))
	public_key = pow(DH_param.g, private_key, DH_param.p)
	
	return Key(DH_param, public_key, private_key)

def DH_comm_estab_Bob(DH_param, client_public_key):
	private_key = random.randint (2, DH_param.q)
	
	pub_key = pow(DH_param.g, private_key, DH_param.p)

	com_key = pow(client_public_key, private_key, DH_param.p)

	return com_key, pub_key, private_key

def DH_comm_estab_Alice(DH_param, server_pub_key, my_private_key):
	return pow(server_pub_key, my_private_key, DH_param.p)


###########################################

def Diffie_Hellman(lenth_q=64, lenth_p=128): # DEPRECIATED
	depth = get_depth()

	print ("{}Diffie_Hellman: function starting".format(depth*"\t"))

	q,p = Schnorr_prime(lenth_q,lenth_p)
	# print ("q : {}".format(q))
	# print ("p : {}".format(p))
	print ("{}Diffie_Hellman: generate g".format(depth*"\t"))
	g = 1
	real_gen = False
	# h = 2
	expo = int((p-1)/q)
	# print (expo)
	while True :
		h = random.randint (2, p-2)
		g = pow (h, expo, p)
		# if g!= 1:
		# 	break
		real_gen = (pow (g, q, p) == 1)
		# sys.stdout.write(ERASE_LINE)
		# print ("{}\t h: {}  real_gen : {}".format(depth*"\t", h, real_gen), end='\r')
		# if g != 1 and real_gen:
		if g != 1:
			print("")
			break
		# else:
		# 	h += 1
	return DHParams(p,q,g)

if __name__ == '__main__':
	main()