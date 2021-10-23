import hashlib
import string
import os
flag_char = []
for i in range (0, 14):
    flag_char.append(0x30)
    
flag_char[0]= 0x45 # ok
flag_char[1]= 0x34 # ok
flag_char[2]= 0x51 # ok
flag_char[3]= 0x35 # ok
flag_char[5]= 0x36 # ok
flag_char[6]= 0x66 # ok
flag_char[7]= 0x60 # ok
flag_char[8]= 115 # ok
flag_char[9]= 52 # ok
flag_char[10] = 108 # ok 
flag_char[11] = 68 # ok
flag_char[12] = 0x35 # ok
flag_char[13] = 25+7+2+6+4+1+19+9 # ok

ALPHABET = string.printable
for c in ALPHABET:
    flag_char[4]= ord(c)
    flag = bytearray(flag_char)
  
    result = hashlib.sha256(flag)
    print("FLAG: %s - SHA256: %s" % (flag.decode(), result.hexdigest()))

    if result.hexdigest() == "b3c20caa9a1a82add9503e0eac43f741793d2031eb1c6e830274ed5ea36238bf":
        print("Found")
        break