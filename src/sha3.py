#!/usr/bin/env python3


path = '../files/lorem.txt'
# val = 0x60aa8b58266a4165e8c9b7f2125ce5f875fdcfc913cb0e2ee38558aa7e0df8

def sha3(file_in, size):
	# size : bits
	# chunk_size = 200 - size // 4 # octets
	chunk_size = 1600 - 2 * size # bits
	# print (chunk_size)
	# print (chunk_size//8)
	with open(file_in, 'rb') as f:
		for chunk in iter(lambda: f.read(chunk_size//8), b''):
			chunk = list(chunk)


			if len(chunk) != chunk_size//8:
				chunk.append(0x06)

				# Appending padding bytes until message is exactly a multiple of a whole block
				while len(chunk) % chunk_size//8 != 0:
					chunk.append(0x00)

				# Set the final bit
				chunk[-1] |= 0x80

			hash_matrix = [ [0] * 5 for _ in range(5)]
			# function
		#restore




		#result
		print( size )
		print(chunk_size) #bits
		print(chunk_size + 2*size) #bits
		# print(size / chunk_size)
		a = size / chunk_size
		print(a)

		print (a * chunk_size)


def main():
	sha3(path, 512)

if __name__ == '__main__':
	main()