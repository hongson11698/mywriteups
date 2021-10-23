import idaapi
desc1 = "frightening, virtual, danish, flimsy, gruesome great, dark oppressive, bad, average, virtual, last, more strange, inhospitable, slimy, average, few dismal".split(", ")
desc2 = "flimsy, gruesome great, dark oppressive, bad, average, virtual, last, more strange, inhospitable, slimy, average, few dismal, flimsy, dark and gruesome, inhospitable, inhospitable, frightening, last, slimy, nicest, solid, dark oppressive, few dismal, deep subterranean, last, gruesome great, average, gruesome great, average, cruel, damned, common, bad".split(", ")


DescriptionTableAddr = 0x94FB00
DescriptionTableSize = 744 

DescriptionTable = []
for i in range(0, DescriptionTableSize):
    Description = idaapi.get_qword(DescriptionTableAddr + i*16)
    DescriptionSize = idaapi.get_qword(DescriptionTableAddr + i*16 + 8)
    DescriptionTable.append(idaapi.get_bytes(Description, DescriptionSize).decode("utf-8"))
print("DescriptionTable = %s" % str(DescriptionTable))

DescByte1 = bytearray("", "utf-8")
for i in range(0, len(desc1)):
    index = DescriptionTable.index(desc1[i])
    DescByte1.append(index)
    
print("DescByte1: %s" % str(DescByte1))

DescByte2 = bytearray("", "utf-8")
for i in range(0, len(desc2)):
    index = DescriptionTable.index(desc2[i])
    DescByte2.append(index)
    
print("DescByte2: %s" % str(DescByte2))