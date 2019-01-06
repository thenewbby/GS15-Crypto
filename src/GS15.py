#!/usr/bin/env python3

from crypto_utils import *
from diffie_hellman import *
from IDEA import *
from DSA import *

import os

# menu = 0
alice_key = None
bob_key = None
com_key = None

def main():
	
	if not os.path.exists("../keys/"):
		os.makedirs("../keys/")
	if not os.path.exists("../sig/"):
		os.makedirs("../sig/")
	if not os.path.exists("../files/"):
		os.makedirs("../files/")

	while True:
		print("""0) Gérer une clé
1) Cipher
2) Signature
3) Exit""")
		var = eval(input("?: "))

		if var == 0:
			key_menu()
		elif var == 1:
			if com_key:
				cipher()
			else:
				print("Besoin d'une com_key")
				
		elif var == 2:
			signature()
		elif var == 3:
			break
		else:
			print("\nMAUVAISE ENTREE")
		print("\n\n")
		
		
def key_menu():
	global alice_key
	global com_key

	depth = get_depth()
	while True:
		print("""{0}0) Clé asymétrique
{0}1) créer une clé de communication
{0}2) Back""".format(depth*"\t"))

		var = eval(input("?: "))

		if var == 0:
			gen_key()
		elif var == 1:
			if alice_key:
				# diffie_hellman
				# DH_comm_estab_Bob
				# DH_comm_estab_Alice
				com_key_b, bob_key =  DH_comm_estab_Bob(alice_key.param, alice_key.public_key)
				com_key_a = DH_comm_estab_Alice(alice_key, bob_key.public_key)
				if com_key_a == com_key_b:
					com_key = com_key_a
				print("comm key: {}".format(com_key))
				# print("comm key: {}".format(int2bytes(com_key, alice_key.param.lenth[1])))
			else:
				print("Il faut avoir une clé asymétrique")
			
		elif var == 2:
			break
		else :
			print("\nMAUVAISE ENTREE")

def gen_key():
	global alice_key

	depth = get_depth()
	while True:
		print("""{0}0) Crée nouvel clé
{0}1) Ecrire dans un fichier
{0}2) charger depuis un fichier
{0}3) Back""".format(depth*"\t"))

		var = eval(input("?: "))

		if var == 0:
			# get size p & q
			ql = eval(input("La longueur de chiffre q (octets):"))
			pl = eval(input("La longueur de chiffre p (octets):"))
			if ql == 0 and pl == 0:
				alice_key = DH_gen_keys()
			elif ql >= pl:
				print("q supérieur a p")
			elif ql == 0 or pl == 0:
				print("longueur de q ou p est égale a 0")
			else : 
				alice_key = DH_gen_keys(ql, pl)
		elif var == 1:
			#  write get file
			if alice_key:
				name = input("Le nom du fichier (sans l'extension): ../keys/")
				write_yaml(alice_key, "../keys/"+name+".yml")
			else:
				print("Pas de clé à écrire")
			
		elif var == 2:
			#  load get file
			name = input("Le nom du fichier (sans l'extension): ../keys/")
			alice_key = read_yaml("../keys/"+name+".yml")
		elif var == 3:
			break
		else :
			print("\nMAUVAISE ENTREE")
		print(alice_key)

def cipher(): # ToDo Init_vector

	file_in = input("fichier d'entré: ../files/")
	file_in = "../files/"+file_in
	file_out = input("fichier de sortie: ../files/")
	file_out = "../files/"+file_out

	global alice_key

	key = int2bytes(com_key, (com_key.bit_length() + 7) // 8)

	init_vector = None

	depth = get_depth()
	mode = None
	dechiffre = -1
	while mode is None:
		print("""{0}0) ECB
{0}1) CBC
{0}2) PCBC""".format(depth*"\t"))

		var = eval(input("?: "))

		if var == 0:
			mode = ECB
		elif var == 1:
			mode = CBC
		elif var == 2:
			mode = PCBC
		else :
			print("\nMAUVAISE ENTREE")

	if mode != ECB:
		last_mode = mode
		while mode == last_mode:
			print("""{0}0) chiffrement
{0}1) déchiffrent""".format(depth*"\t"))

			var = eval(input("?: "))

			if var == 0:
				mode = mode.cipher
				dechiffre = 0
			elif var == 1:
				mode = mode.decipher
				dechiffre = 1
			else :
				print("\nMAUVAISE ENTREE")

	function = None
	while function is None:
		print("""{0}0) XOR
{0}1) IDEA""".format(depth*"\t"))

		var = eval(input("?: "))

		if var == 0:
			function = bytes_xor_bytes
		elif var == 1:
			function = IDEA(key)
		else :
			print("\nMAUVAISE ENTREE")

	if isinstance(function, IDEA):
		while dechiffre == -1:
			print("""{0}0) chiffrement
{0}1) déchiffrent""".format(depth*"\t"))

			var = eval(input("?: "))

			if var == 0:
				mode = mode.cipher
				dechiffre = 0
			elif var == 1:
				mode = mode.decipher
				dechiffre = 1
			else :
				print("\nMAUVAISE ENTREE")

		while init_vector is None:
			vect = eval(input("vecteur initial (entier entre 0 et 18446744073709551615): "))
			if 0 <= vect and vect <= 18446744073709551615:
				init_vector = int2bytes(vect, 8)
			else :
				print("wrong input")


		if dechiffre:
			mode(function.decipher, file_in, file_out, 8, key, init_vector)
		else:
			mode(function.cipher, file_in, file_out, 8, key, init_vector)
	else:
		mode(function, file_in, file_out, (com_key.bit_length() + 7) // 8, key, init_vector)
	
def signature():
	global alice_key

	depth = get_depth()
	while True:
		print("""{0}0) DSA
{0}1) Back""".format(depth*"\t"))

		var = eval(input("?: "))

		if var == 0:
			dsa()
		elif var == 1:
			break
		else :
			print("\nMAUVAISE ENTREE")


def dsa():
	global alice_key

	depth = get_depth()
	while True:
		print("""{0}0) sign
{0}1) verify
{0}2) Back""".format(depth*"\t"))

		var = eval(input("?: "))

		if var == 0:
			if alice_key:
				msg = input("le message: ")

				sign = DSA_sign(alice_key, msg.encode('utf-8'))

				name = input("le nom du fichier (sans l'extension): ../sig/")
				write_yaml(sign, "../sig/"+name+".yml" )
			else :
				print("Pas de clé à utiliser")

		elif var == 1:
			name = input("le nom du fichier (sans l'extension): ../sig/")
			sign = read_yaml("../sig/"+name+".yml")

			if DSA_verify(sign):
				print("signature vérifié")
			else:
				print("signature eroné")

		elif var == 2:
			break
		else :
			print("\nMAUVAISE ENTREE")


if __name__ == '__main__':
	main()