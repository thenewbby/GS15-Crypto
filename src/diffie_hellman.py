#!/usr/bin/env python3

from crypto_utils import *
import random
import inspect
import sys

# https://www.baylon-industries.com/news/?p=1430
# https://crypto.stackexchange.com/questions/9006/how-to-find-generator-g-in-a-cyclic-group
def main ():

	alice_key = DH_gen_keys()
	com_key_b, B, b =  DH_comm_estab_Bob(alice_key.param, alice_key.public_key)
	com_key_a = DH_comm_estab_Alice(alice_key, B)

	assert com_key_b == com_key_a
	A_hex = int2bytes(com_key_a, 128)
	bytesToString(A_hex)


def DH_gen_keys(lenth_q=64, lenth_p=128):
	"""
	@brief      Génère une clé assymétrique
	
	@param      lenth_q  Longueur en octes de q
	@param      lenth_p  Longueur en octes de p
	
	@return     Un clé assymétrique (Classe Key)
	"""
	depth = get_depth()
	print ("{}DH_gen_keys: function starting".format(depth*"\t"))
	DH_param = Schnorr_group(lenth_q, lenth_p)
	
	print ("{}DH_gen_keys: generate private key".format(depth*"\t"))
	private_key = random.randint (2, DH_param.q)

	print ("{}DH_gen_keys: generate public key".format(depth*"\t"))
	public_key = pow(DH_param.g, private_key, DH_param.p)
	
	return Key(DH_param, public_key, private_key)

def DH_comm_estab_Bob(DH_param, client_public_key):
	"""
	@brief      Génère une clé privé et de communication
	
	@param      DH_param           Les paramètres de la génération de clé
	@param      client_public_key  La clé publique de l'interlocuteur
	
	@return     La clé de communication, publique et privé de bob
	"""
	depth = get_depth()
	print ("{}DH_comm_estab_Bob: function starting".format(depth*"\t"))

	print ("{}DH_comm_estab_Bob: generate private key".format(depth*"\t"))
	private_key = random.randint (2, DH_param.q)

	print ("{}DH_comm_estab_Bob: generate public key".format(depth*"\t"))
	pub_key = pow(DH_param.g, private_key, DH_param.p)
	
	print ("{}DH_comm_estab_Bob: generate com key".format(depth*"\t"))
	com_key = pow(client_public_key, private_key, DH_param.p)

	return com_key, pub_key, private_key

def DH_comm_estab_Alice(my_key, server_pub_key):
	"""
	@brief      Génère la clé de communication du coté d'alice
	
	@param      my_key          Ma clé
	@param      server_pub_key  La clé public du serveur
	
	@return     La clé de communication
	"""
	depth = get_depth()
	print ("{}DH_comm_estab_Alice: generate com key".format(depth*"\t"))
	return pow(server_pub_key, my_key.private_key, my_key.param.p)

if __name__ == '__main__':
	main()