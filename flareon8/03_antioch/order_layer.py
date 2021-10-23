# get ordered layer
from pathlib import Path
import glob
import json
import zlib
import shutil
import tarfile
import os

listCrcOrder = [
    (b"\xa9\x95\x93\xb5", 0x0e),
    (b"\x4b\xd0\xfd\x5e", 0x12),
    (b"\xd0\x85\xed\xec", 0x02),
    (b"\x14\x92\x54\xd8", 0x1d),
    (b"\x4d\x02\x2f\x2c", 0x0c),
    (b"\x32\x52\x8a\x01", 0x0d),
    (b"\x33\x8a\xb8\x72", 0x14),
    (b"\xe2\x04\x44\x67", 0x0b),
    (b"\xb5\x73\x7a\x30", 0x1c),
    (b"\x04\x87\x46\x13", 0x15),
    (b"\x1b\x47\xf6\x94", 0x05),
    (b"\x75\xcf\xa1\xed", 0x18),
    (b"\x4d\x12\xac\xbb", 0x19),
    (b"\xc3\xe4\x07\xf7", 0x07),
    (b"\x6f\x59\x02\xd7", 0x0a),
    (b"\x48\x08\xa1\x86", 0x01),
    (b"\x1c\x53\x40\xd6", 0x13),
    (b"\xb3\x5d\x66\x7b", 0x03),
    (b"\xcc\x21\x13\xab", 0x04),
    (b"\xd8\x66\x60\x4f", 0x11),
    (b"\xca\x47\x60\x25", 0x09),
    (b"\xd3\x1e\xc9\x3f", 0x08),
    (b"\xe4\xaf\x24\xa4", 0x1b),
    (b"\xda\x01\x09\x55", 0x10),
    (b"\x2d\x9e\xa2\x10", 0x16),
    (b"\x5f\xc8\xcb\x56", 0x0f),
    (b"\xa6\xe3\xdf\x80", 0x1e),
    (b"\xe1\xd4\x57\xe6", 0x17),
    (b"\xd4\xe1\xa1\x2b", 0x1a),
    (b"\x9b\x08\x33\x7d", 0x06)
]
def sec_elem(s):
    return s[1]

listCrcOrder = sorted(listCrcOrder, key=sec_elem)
dest = Path("ordered")
shutil.copy2("AntiochOS", dest)

for crc in listCrcOrder:
    for path in glob.glob('antioch/**/json'):
        with open(path, "r") as f:
            jsonData = json.loads(f.read())
            if "author" in jsonData:
                authorByte = (jsonData["author"] + '\n').encode()
                crcName = (zlib.crc32(authorByte) & 0xffffffff)
                if int.from_bytes(crc[0], "little") == crcName:
                    print("Author: %s - 0x%x - order: %d" % (str(authorByte), crcName, crc[1]))
                    srcLayer = Path(path).parent.joinpath("layer.tar")
                    print("Get source layer %s" % srcLayer)
                    my_tar = tarfile.open(srcLayer)
                    my_tar.extractall(dest) # specify which folder to extract to
                    my_tar.close()
print("Ordered. Run Antioch with consult command to get flag")
