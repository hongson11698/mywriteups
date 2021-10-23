import sys
def decodeText(ENCODED_BYTE):
    return ENCODED_BYTE + 27 + 2 * 3 - 37

if len(sys.argv) == 2:
    with open(sys.argv[1], "rb") as f:
        data = f.read()
        decode = bytearray()
        for c in data:
            if c == 0:
                break
            decode.append(decodeText(c))
        print(decode)