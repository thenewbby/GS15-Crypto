#!/usr/bin/env python3

from crypto_utils import *
import random

# https://www.baylon-industries.com/news/?p=1430
# https://crypto.stackexchange.com/questions/9006/how-to-find-generator-g-in-a-cyclic-group

def main ():
	p, g = Diffie_Hellman()

	secret_a = random.randint (2, 100)
	secret_b = random.randint (2, 100)

	A = g**secret_a % p
	B = g**secret_b % p

	B = B**secret_a % p
	A = A**secret_b % p

	# print (A)
	# print (B)
	assert A == B

	A_hex = int2bytes(A, 128)
	print (A_hex)


def Diffie_Hellman():
	q,p = Schnorr_prime()
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
	return p,g

def Schnorr_prime():
	# i = 1
	q = 0
	while True:
		# q = bytes2int(genKey(3, False))
		q = bytes2int(genKey(64, False))
		# print (key)
		# print (is_prime(key))
		if is_prime(q):
			break
		# else:
		# 	i += 1
	# print (i)
	p = 0
	h = bytes2int(genKey(64, False))
	# i = 0
	while True:
		p = h * q + 1
		if is_prime(p):
			break
		else:
			h = bytes2int(genKey(64, False))
			# i += 1
	# print (i)
	return q,p

if __name__ == '__main__':
	main()