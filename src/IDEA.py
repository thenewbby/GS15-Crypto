#!/usr/bin/env python3

# BASED ON OTHER PROJECT
# 
# The IDEA (International Data Encryption Algorithm) block cipher.
# 
# Copyright (c) 2018 Project Nayuki. (MIT License)
# https://www.nayuki.io/page/cryptographic-primitives-in-plain-python
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# - The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
# - The Software is provided "as is", without warranty of any kind, express or
#   implied, including but not limited to the warranties of merchantability,
#   fitness for a particular purpose and noninfringement. In no event shall the
#   authors or copyright holders be liable for any claim, damages or other
#   liability, whether in an action of contract, tort or otherwise, arising from,
#   out of or in connection with the Software or the use or other dealings in the
#   Software.


from crypto_utils import *

# ---- Numerical constants/tables ----

_NUM_ROUNDS = 8

def main():
	key = int2bytes(0x2BD6459F82C5B300952C49104881FF48, 16)
	plain = int2bytes(0xF129A6601EF62A47, 8)
	cip = int2bytes(0xEA024714AD5C4D84, 8)


	idea = IDEA(key)

	print ("encrypt: ")

	print (idea.encrypt(plain, key))
	print (cip)
	assert idea.encrypt(plain, key) == cip

	print ("\ndecrypt: ")
	print (idea.decrypt(cip, key))
	print (plain)
	assert idea.decrypt(cip, key) == plain


class IDEA(object):
	"""Classe pour le chiffrement IDEA"""

	def __init__(self, key):
		self.update_key(key)

	def encrypt(self, chunk, key):
		"""
		@brief      Chiffre le bloc avec la clé passé en paramettre
		
		@param      self   L'object
		@param      chunk  Le bloc
		@param      key    La clé
		
		@return     Retourne le bloc chiffré
		"""

		if list(key) != self.key:
			self.update_key(key)
		return self.cipher(chunk, self.key_exanted)

	def decrypt(self, chunk, key):
		"""
		@brief      Déchiffre le bloc avec la clé passé en paramettre
		
		@param      self   L'object
		@param      chunk  Le bloc
		@param      key    La clé
		
		@return     Retourne le bloc déchiffré
		"""
		if list(key) != self.key:
			self.update_key(key)
		return self.cipher(chunk, self.reversed_key)

	def update_key(self, key):
		"""
		@brief      Mets à jours les clé interne
		
		@param      self  L'object
		@param      key   La clé
		
		"""
		self.key = list(key)
		assert isinstance(self.key, list) and len(self.key) >= 16
		self.key_exanted = self.expand_key(key[:16])
		self.reversed_key = self.reverse_key()
		
	@staticmethod
	def cipher(chunk, key_used):
		"""
		@brief      Chiffre ou déchiffre le bloc avec la clé passé en paramètre
		
		@param      chunk     Le bloc
		@param      key_used  La clé
		
		@return     le bloc chiffré ou déchiffré
		"""
		chunk = list(chunk)

		assert isinstance(chunk, list) and len(chunk) == 8

		# Pack chunk bytes into variables as uint16 in big endian
		w = chunk[0] << 8 | chunk[1]
		x = chunk[2] << 8 | chunk[3]
		y = chunk[4] << 8 | chunk[5]
		z = chunk[6] << 8 | chunk[7]
		
		# Perform 8 rounds of encryption/decryption
		for i in range(_NUM_ROUNDS):
			j = i * 6
			w = _multiply(w, key_used[j + 0])
			x = _add(x, key_used[j + 1])
			y = _add(y, key_used[j + 2])
			z = _multiply(z, key_used[j + 3])
			u = _multiply(w ^ y, key_used[j + 4])
			v = _multiply(_add(x ^ z, u), key_used[j + 5])
			u = _add(u, v)
			w ^= v
			x ^= u
			y ^= v
			z ^= u
			x, y = y, x
		
		# Perform final half-round
		x, y = y, x
		w = _multiply(w, key_used[-4])
		x = _add(x, key_used[-3])
		y = _add(y, key_used[-2])
		z = _multiply(z, key_used[-1])
		
		# Serialize the final chunk as a bytelist in big endian
		return bytes([
			w >> 8, w & 0xFF,
			x >> 8, x & 0xFF,
			y >> 8, y & 0xFF,
			z >> 8, z & 0xFF])

	def expand_key(self, key):
		"""
		@brief      Expand la clé pour le chiffrement IDEA
		
		@param      self  L'object
		@param      key   La clé
		
		@return     La clé étendue
		"""
		# Pack all key bytes into a single uint128
		bigkey = 0
		for b in key:
			assert 0 <= b <= 0xFF
			bigkey = (bigkey << 8) | b
		assert 0 <= bigkey < (1 << 128)
		
		# Append the 16-bit prefix onto the suffix to yield a uint144
		bigkey = (bigkey << 16) | (bigkey >> 112)
		
		# Extract consecutive 16 bits at different offsets to form the key schedule
		result = []
		for i in range(_NUM_ROUNDS * 6 + 4):
			offset = (i * 16 + i // 8 * 25) % 128
			result.append((bigkey >> (128 - offset)) & 0xFFFF)
		return tuple(result)


	def reverse_key(self):
		"""
		@brief      Inverse la clé pour le déchiffrement
		
		@param      self  L'object
		
		@return     La clé inversé
		"""
		assert isinstance(self.key_exanted, tuple) and len(self.key_exanted) % 6 == 4
		result = []
		result.append(_reciprocal(self.key_exanted[-4]))
		result.append(_negate(self.key_exanted[-3]))
		result.append(_negate(self.key_exanted[-2]))
		result.append(_reciprocal(self.key_exanted[-1]))
		result.append(self.key_exanted[-6])
		result.append(self.key_exanted[-5])
		
		for i in range(1, _NUM_ROUNDS):
			j = i * 6
			result.append(_reciprocal(self.key_exanted[-j - 4]))
			result.append(_negate(self.key_exanted[-j - 2]))
			result.append(_negate(self.key_exanted[-j - 3]))
			result.append(_reciprocal(self.key_exanted[-j - 1]))
			result.append(self.key_exanted[-j - 6])
			result.append(self.key_exanted[-j - 5])
		
		result.append(_reciprocal(self.key_exanted[0]))
		result.append(_negate(self.key_exanted[1]))
		result.append(_negate(self.key_exanted[2]))
		result.append(_reciprocal(self.key_exanted[3]))
		return tuple(result)

# ---- Private arithmetic functions ----

# Returns x + y modulo 2^16. Inputs and output are uint16. Only used by cipher().
def _add(x, y):
	assert 0 <= x <= 0xFFFF
	assert 0 <= y <= 0xFFFF
	return (x + y) & 0xFFFF


# Returns x * y modulo (2^16 + 1), where 0x0000 is treated as 0x10000.
# Inputs and output are uint16. Note that 2^16 + 1 is prime. Only used by cipher().
def _multiply(x, y):
	assert 0 <= x <= 0xFFFF
	assert 0 <= y <= 0xFFFF
	if x == 0x0000:
		x = 0x10000
	if y == 0x0000:
		y = 0x10000
	z = (x * y) % 0x10001
	if z == 0x10000:
		z = 0x0000
	assert 0 <= z <= 0xFFFF
	return z


# Returns the additive inverse of x modulo 2^16.
# Input and output are uint16. Only used by reverse_key().
def _negate(x):
	assert 0 <= x <= 0xFFFF
	return (-x) & 0xFFFF


# Returns the multiplicative inverse of x modulo (2^16 + 1), where 0x0000 is
# treated as 0x10000. Input and output are uint16. Only used by reverse_key().
def _reciprocal(x):
	assert 0 <= x <= 0xFFFF
	if x == 0:
		return 0
	else:
		return pow(x, 0xFFFF, 0x10001)  # By Fermat's little theorem


	

if __name__ == '__main__':
	main()