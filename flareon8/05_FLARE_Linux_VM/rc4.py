from Crypto.Cipher import ARC4
import sys
import base64
key = ARC4.new('493513')
if len(sys.argv) == 2:
    with open(sys.argv[1], "rb") as f:
        data = key.decrypt(f.read())
        print(data)