#!/usr/bin/env python3

from crypto_utils import *
import random

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

	DH_param, A, a = DH_gen_public_key()
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
	

	
def DH_gen_public_key():
	DH_param = Diffie_Hellman()
	# private_key = random.randint (2, DH_param[1])
	private_key = random.randint (2, 10)
	# public_key = DH_param[1]**private_key % DH_param[0]
	public_key = pow(DH_param[2], private_key, DH_param[0])
	return DH_param, public_key, private_key

def DH_comm_estab_Bob(DH_param, client_public_key):
	# private_key = random.randint (2, DH_param[1])
	private_key = random.randint (2, 10)
	# pub_key = DH_param[2]**private_key % DH_param[0]
	pub_key = pow(DH_param[2], private_key, DH_param[0])

	# com_key = client_public_key**private_key % DH_param[0]
	com_key = pow(client_public_key, private_key, DH_param[0])
	return com_key, pub_key, private_key

def DH_comm_estab_Alice(DH_param, server_pub_key, my_private_key):
	# return server_pub_key**my_private_key % DH_param[0]
	return pow(server_pub_key, my_private_key, DH_param[0])
	# return B**secret_a % public_key[2]


###########################################

def Diffie_Hellman():
	q,p = Schnorr_prime(64,128)
	# print ("q : {}".format(q))
	# print ("p : {}".format(p))
	g = 1
	while g == 1:
		h = random.randint (2, p-1)
		expo = int((p-1)/q)
		# print ((p-1)/q)
		# print (h**((p-1)/q))
		# g = (h**expo)%p
		g = pow (h, expo, p)
	# print ("g : {}".format(g))
	return (p,q,g)

if __name__ == '__main__':
	main()