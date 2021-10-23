rom3Index = 0
def cpu5(data):
    global rom3Index
    rData = rom3[rom3Index]
    if rom3Index & 1 == 1:
        rData = (rData ^ 0xffffffff) & 0xff
    data = data ^ rData
    rom3Index = (rom3Index + 1) % len(rom3)
    return data

def cpu4(data):
    data = data - 200
    data = rom2[data]
    return data

def cpu3(data):
    if (data > 199):
        data = cpu4(data)
    else:
        data = data - 100
        data = rom1[data]
    return data

def cpu2(data):
    if data > 99:
        data = cpu3(data)
    else:
        data = rom0[data]
    return data
    
def cpu1(data):
    data = cpu2(data)
    data = cpu5(data)
    data = cpu2(data)
    if data & 128 == 128:
        data = data ^ 66
    data = (data ^ 0xffffffff) & 0xff
    return data

def cpu0(data):
    outData = cpu1(data)
    return outData 

rom0=[90, 132, 6, 69, 174, 203, 232, 243, 87, 254, 166, 61, 94, 65, 8, 208, 51, 34, 33, 129, 32, 221, 0, 160, 35, 175, 113, 4, 139, 245, 24, 29, 225, 15, 101, 9, 206, 66, 120, 62, 195, 55, 202, 143, 100, 50, 224, 172, 222, 145, 124, 42, 192, 7, 244, 149, 159, 64, 83, 229, 103, 182, 122, 82, 78, 63, 131, 75, 201, 130, 114, 46, 118, 28, 241, 30, 204, 183, 215, 199, 138, 16, 121, 26, 77, 25, 53, 22, 125, 67, 43, 205, 134, 171, 68, 146, 212, 14, 152, 20]
rom1=[185, 155, 167, 36, 27, 60, 226, 58, 211, 240, 253, 79, 119, 209, 163, 12, 72, 128, 106, 218, 189, 216, 71, 91, 250, 150, 11, 236, 207, 73, 217, 17, 127, 177, 39, 231, 197, 178, 99, 230, 40, 54, 179, 93, 251, 220, 168, 112, 37, 246, 176, 156, 165, 95, 184, 57, 228, 133, 169, 252, 19, 2, 81, 48, 242, 105, 255, 116, 191, 89, 181, 70, 23, 194, 88, 97, 153, 235, 164, 158, 137, 238, 108, 239, 162, 144, 115, 140, 84, 188, 109, 219, 44, 214, 227, 161, 141, 80, 247, 52]
rom2=[213, 249, 1, 123, 142, 190, 104, 107, 85, 157, 45, 237, 47, 147, 21, 31, 196, 136, 170, 248, 13, 92, 234, 86, 3, 193, 154, 56, 5, 111, 98, 74, 18, 223, 96, 148, 41, 117, 126, 173, 233, 10, 49, 180, 187, 186, 135, 59, 38, 210, 110, 102, 200, 76, 151, 198]
rom3=[97, 49, 49, 95, 109, 89, 95, 104, 111, 109, 49, 101, 115, 95, 104, 52, 116, 51, 95, 98, 52, 114, 100, 115]

def encrypt(data):
    return cpu0(data)

#print(encrypt(0x6a))
#rom3Index = 0
#png = [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]
#for i in range(0, len(png)):
#    print(hex(encrypt(png[i])))
#exit(0)

out = bytearray()
with open("res.png", "rb") as f:
    png = f.read()
for i in range(0, len(png)):
    currentIdx = i%len(rom3)
    for j in range(0, 256):
        rom3Index = currentIdx
        expected = encrypt(j)
        if expected == png[i]:
            out.append(j)
            #input("Check byte[%d]: encrypt(%x) = %x" % (i, j, expected))
            break
    print("Got 0x%x byte" % i)
with open("out.png", "wb") as f:
    f.write(out) 

       