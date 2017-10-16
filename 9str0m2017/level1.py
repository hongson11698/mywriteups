decode = "S2^g1s^c2f0o2s  "
flag = ""
for c in decode:
    flag += chr(ord(c) ^ 1)


print "Nightst0rm{%s}" % flag
#Nightst0rm{R3_f0r_b3g1n3r!!}
