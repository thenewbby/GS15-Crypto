#!/usr/bin/env python3

import os
import sys
import re
import random
import binascii
import crypto_utils
from functools import reduce


"""
print in binary : https://stackoverflow.com/questions/8815592/convert-bytes-to-bits-in-python
"""


def main():
	inp = input("number of bytes: ")
	print ()
	rand = os.urandom(int(inp))
	print ("\trandom bytes generated: {}".format(rand))

	# print (rand[0])


	# rand_hex = ':'.join(hex(ord(x))[2:] for x in rand) #python2
	rand_hex = rand.hex()
	rand_hex = ':'.join(a+b for a,b in zip(rand_hex[::2], rand_hex[1::2]))
	# rand_hex = rand_hex[:4] + 'z' + rand_hex[4:]
	print ("\trandom bytes as beautifull hexa: {}".format(rand_hex))

	# print (type(rand_hex))
	# print (rand_hex)
	# r = re.compile('^([0-9a-f]{2}:)*[0-9a-f]{2}$')
	# print (r.match(rand_hex))
	print ("\nParsing\n")
	if re.match('^([0-9a-f]{2}:)*[0-9a-f]{2}$', rand_hex) is not None:
		hexa = rand_hex.replace(":", "")
		byt = binascii.unhexlify(hexa)
		# print ("binascii : {}".format(binascii.unhexlify(hexa)))
		print ("\tbytes found after parsing beautiful hexa: {}".format(byt))
		assert (byt == rand)


	else:
		print ("\tWrong key structure")


	sliding = random.randint(1, len(rand)*8 - 1)

	print ("\nBinary rotation\n")

	print ("\tfirst: left {} times".format(sliding))


	print ("\tkey binary format: {}".format(bin(int(rand.hex(), base=16)).lstrip('0b')))
	temp = int.from_bytes(rand, byteorder='big')

	print ("\tint format of the key: {}".format(temp))
	temp = crypto_utils.rol(temp,sliding , len(rand)*8)
	print ("\tint after sliding: {}".format(temp))


	rnd = temp.to_bytes(len(rand), byteorder='big')
	print ("\tkey binary format: {}".format(bin(int(rnd.hex(), base=16)).lstrip('0b')))
	print ("\tkey in bytes: {}".format(rnd))
	
	print ("\tsecond: right {} times".format(sliding))
	temp = crypto_utils.ror(temp,sliding , len(rand)*8)
	print ("\tint after sliding: {}".format(temp))

	rnd0 = temp.to_bytes(len(rand), byteorder='big')
	print ("\tkey binary format: {}".format(bin(int(rnd0.hex(), base=16)).lstrip('0b')))
	print ("\tkey in bytes: {}".format(rnd))


	assert (rand == rnd0)


	rnd1 = crypto_utils.bytes_rol(rand, sliding)

	assert (rnd1 == rnd)

	rnd2 = crypto_utils.bytes_ror(rnd, sliding)

	assert (rand == rnd2)

	# print ()
	# ran = crypto_utils.bytes2int(rand)
	# ran2 = crypto_utils.rol(ran, 5 , len(rand)*8)
	# an = ran | ran2
	# print ("key binary format: {}".format(bin(ran).lstrip('0b')))
	# print ("key binary format: {}".format(bin(ran2).lstrip('0b')))
	# print ("key binary format: {}".format(bin(an).lstrip('0b')))

	# print ("and operator: {}".format(an))

	print ("miller-rabin")
	x = random.randint(1, 99999999999999999)
	print(" {} is prime ? : {}".format(x, crypto_utils.is_prime(x)))
	print(" {} is prime ? : {}".format(997, crypto_utils.is_prime(997)))
	# print("prime range [{},{}] : {}".format(1, 100000, [x for x in range(1, 100000) if crypto_utils.is_prime(x)] ))
	# print ("known prime {}".format(crypto_utils._known_primes))
	
	print ()
	# print ("factorize 1561559131521824685 : {}".format(crypto_utils.factorize(1561559131521824685)))
	temp = crypto_utils.factorize(x)
	print ("factorize {} : {}".format(x, temp))
	tm = reduce(lambda x, y: x*y, temp)
	print ("mult : {}".format(tm))
	print ("diff {}".format(x - tm))
	assert (x == reduce(lambda x, y: x*y, temp))

if __name__ == '__main__':
	main()