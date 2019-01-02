#!/usr/bin/env python3

from crypto_utils import *
import IDEA

# path = '../files/lorem.txt'
# path_sec = '../files/lorem_sec.txt'
# path_unsec = '../files/lorem_unsec.txt'

path = '../files/long_lorem.txt'
path_sec = '../files/long_lorem_sec.txt'
path_unsec = '../files/long_lorem_unsec.txt'

# path = '../files/moi.jpg'
# path_sec = '../files/moi_sec.jpg'
# path_unsec = '../files/moi_unsec.jpg'

chunkSize = 8
key = int2bytes(55, 16)
in_vect = int2bytes(165, chunkSize)


def main():
    idea = IDEA.IDEA(key)

    ECB(idea.encrypt, path, path_sec, chunkSize, key)
    ECB(idea.decrypt, path_sec, path_unsec, chunkSize, key)
    # ECB(idea.encrypt, path, path_sec, chunkSize, key)
    # ECB(idea.decrypt, path_sec, path_unsec, chunkSize, key)

    # CBC.cipher(idea.encrypt, path, path_sec, chunkSize, key, in_vect)
    # CBC.decipher(idea.decrypt, path_sec, path_unsec, chunkSize, key, in_vect)

    # PCBC.cipher(idea.encrypt, path, path_sec, chunkSize, key, in_vect)
    # PCBC.decipher(idea.decrypt, path_sec, path_unsec, chunkSize, key, in_vect)


if __name__ == '__main__':
    main()
