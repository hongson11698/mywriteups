from z3 import *
s = Solver()
secret = "304A41053D551E013540761C080255082503070C27026822".decode("hex")
byte_41A000 = "0123456789+/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
block2 = "015C272D0C590D32".decode('hex')
block3 = "4B0144614642686A".decode('hex')
pass_block2 = "khangkit"
pass_block3 = "12121212"

input1 = "iz4ZJapu"
input2 = ""
input3 = ""
_input = ""
flag = ""
input = []
for i in xrange(0, 10):
    input.append(BitVec('input%d'%i, 8))
	

for i in xrange(0, 3):
    s.add(input[i] >= 0x20)
    s.add(input[i] <= 0x7d) 
result = list("olCOkyDvq7i=")

i = 0
j = 0
while (j < len(result)):
	s.add(LShR(input[i], 2) == byte_41A000.index(result[j]))
	s.add((LShR(input[i+1]&0xF0, 4) | 16 * (input[i]&3)) == byte_41A000.index(result[j+1]))
	if(result[j+2] != '='):
		s.add((LShR(input[i+2]&0xC0, 6) | 4 * (input[i+1]&0xF)) == byte_41A000.index(result[j+2]))
	if(result[j+3] != '='):
		s.add((input[i+2]&0x3F) == byte_41A000.index(result[j+3]))
	i+=3
	j+=4
if (str(s.check()) == "sat"):
	#print s.model()
	print "OK!"
else:
	print s.check()
#input1 = "iz4ZJapu"
for i in xrange(0, 8):
	input2 += chr(ord(pass_block2[i]) ^ ord(block2[i]))
for i in xrange(0, 8):
	input3 += chr(ord(pass_block3[i]) ^ ord(block3[i]))
_input += input1+input2+input3
for i in xrange(0, 24):
	flag += chr(ord(_input[i]) ^ ord(secret[i]))
print "Input is: %s" % _input
print "NightStr0m{%s}" % flag
