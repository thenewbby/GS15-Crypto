#!/usr/bin/env python3

from crypto_utils import *
import random
import inspect

# https://www.baylon-industries.com/news/?p=1430
# https://crypto.stackexchange.com/questions/9006/how-to-find-generator-g-in-a-cyclic-group

def main ():
	# p,q, g = Diffie_Hellman()

	# secret_a = random.randint (2, 100)
	# secret_b = random.randint (2, 100)

	# A = g**secret_a % p
	# B = g**secret_b % p

	# B = B**secret_a % p
	# A = A**secret_b % p

	# # print (A)
	# # print (B)
	# assert A == B

	# A_hex = int2bytes(A, 128)
	# print (A_hex)

	DH_param, A, a = DH_gen_keys()
	# print (DH_param)
	# print (A)
	# print (a)
	# print()
	com_key_b, B, b =  DH_comm_estab_Bob(DH_param, A)
	# print (com_key_b)
	# print (B)
	# print (b)
	# print()
	com_key_a = DH_comm_estab_Alice(DH_param, B, a)

	assert com_key_b == com_key_a
	A_hex = int2bytes(com_key_a, 128)
	print (A_hex)
	


def DH_gen_keys(lenth_q=64, lenth_p=128):
	depth = get_depth()
	print ("{}DH_gen_keys: function starting".format(depth*"\t"))
	DH_param = Diffie_Hellman(lenth_q, lenth_p)
	
	print ("{}DH_gen_keys: generate private key".format(depth*"\t"))
	private_key = random.randint (1, DH_param.q)

	print ("{}DH_gen_keys: generate public key".format(depth*"\t"))
	public_key = pow(DH_param.g, private_key, DH_param.p)
	
	return DH_param, public_key, private_key

def DH_comm_estab_Bob(DH_param, client_public_key):
	private_key = random.randint (2, DH_param.q)
	
	pub_key = pow(DH_param.g, private_key, DH_param.p)

	com_key = pow(client_public_key, private_key, DH_param.p)

	return com_key, pub_key, private_key

def DH_comm_estab_Alice(DH_param, server_pub_key, my_private_key):
	return pow(server_pub_key, my_private_key, DH_param.p)


###########################################

def Diffie_Hellman(lenth_q=64, lenth_p=128):
	depth = get_depth()

	print ("{}Diffie_Hellman: function starting".format(depth*"\t"))

	q,p = Schnorr_prime(lenth_q,lenth_p)
	# print ("q : {}".format(q))
	# print ("p : {}".format(p))
	print ("{}Diffie_Hellman: generate g".format(depth*"\t"))
	g = 1
	while g == 1:
		h = random.randint (2, p-1)
		expo = int((p-1)/q)
		g = pow (h, expo, p)
	return DHParams(p,q,g)

if __name__ == '__main__':
	main()