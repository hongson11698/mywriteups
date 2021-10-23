# Rotate left: 0b1001 --> 0b0011
rol = lambda val, r_bits, max_bits: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))

# Rotate right: 0b1001 --> 0b1100
ror = lambda val, r_bits, max_bits: \
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))

png_header = [137, 80, 78, 71, 13, 10, 26, 10]
with open("Files/capa.png.encrypted", "rb") as f_enc:
    enc_header = f_enc.read(8)

key = bytearray()
for i in range(0, 8):
    key.append(ror(png_header[i]+i, i, 8) ^ enc_header[i])
print("Key: %s" % key.decode("utf-8"))

with open("Files/critical_data.txt.encrypted", "rb") as f_enc:
    critical_data = f_enc.read()

flag = ""
for i in range(0, len(critical_data)):
    flag += chr(rol(critical_data[i] ^ key[i%8], i%8, 8) - i%8)
print("Flag: %s" % flag)
