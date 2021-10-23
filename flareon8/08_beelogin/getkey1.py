from z3 import *
import base64
import string

with open("b64Data1", "rb") as f1:
    base64Data1 = f1.read()
with open("b64Data2", "rb") as f2:
    base64Data2 = f2.read()

#print(base64Data1)
#print(base64Data2)
set_option("parallel.enable", True)
set_param("parallel.enable", True)

s = z3.Solver()
k = "ChVCVYzI1dU9cVg1ukBqO2u4UGr9aVCNWHpMUuYDLmDO2*cdhXq3oqp8jmKBHU*I"      
keys = []
setChar = bytearray(string.printable, "utf-8")
for i in range (0,64):
    keys.append(z3.BitVec("k_%d" %i, 8))
    s.add(keys[i] >= 0)
    s.add(keys[i] <= 127)   
    for j in range(0, 128):
        if j not in setChar:
            s.add(keys[i] != j)
    s.add(keys[i] != 0xb)
    s.add(keys[i] != 0xc)
    if (k[i] != '*'):
        s.add(keys[i] == ord(k[i]))
#print(keys)
# some addition result for key:
b2Key = []
for i in range(0, len(base64Data2)):
    b2Key.append((base64Data2[i] + keys[i%len(keys)]) & 0xFF)
#print(b2Key)        

b1Data = []
for i in range(0, 0x1000):  
    b1Data.append((base64Data1[i] - b2Key[i%len(b2Key)]) & 0xFF)
    s.add(b1Data[i] >= 0)
    s.add(b1Data[i] <= 127)   
    for j in range(0, 128):
        if j not in setChar:
            s.add(b1Data[i] != j)
    s.add(b1Data[i] != 0xb)
    s.add(b1Data[i] != 0xc)
#print(b1Data)
s.add(b1Data[0] == 0x2f)
s.add(b1Data[1] == 0x2f)

with open("result_test.txt", "rb") as f:
    out = f.read(0xb50)
    i = 2
    while (i < len(out)):
        if (out[i] == 0x0d):
            print(out[i:])
            s.add(b1Data[i+1] == 0x0a)
            s.add(b1Data[i+2] == 0x2f)
            s.add(b1Data[i+3] == 0x2f)
            i+=4
        i+=1
        
t = 0
keyOut = []
while (s.check() == z3.sat):
    m = s.model()
    key1Str = ""
    for n in keys:
        key1Str += chr(m[n].as_long())
    if (key1Str in keyOut):
        continue
    keyOut.append(key1Str)
    print(key1Str)
    l_b2Data = list(base64Data2)
    #print(l_b2Data)
    for i in range(0, len(l_b2Data)):
        l_b2Data[i] = (l_b2Data[i] + ord(key1Str[i%len(key1Str)])) & 0xFF
    #print(l_b2Data)
    
    l_b1Data = list(base64Data1)
    #print(l_b1Data)
    for i in range(0, len(base64Data1)):  
        l_b1Data[i] = (l_b1Data[i] - l_b2Data[i%len(l_b2Data)]) & 0xFF
    outData = ""
    for a in l_b1Data:
        outData += chr(a)
    with open("step1\\result_%d.txt" % t, "wb") as f:
        f.write(bytearray("Key: %s\nOutData:\n%s" % (key1Str, outData), "utf-8"))
    t+=1
