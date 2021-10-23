from collections import Counter
import math
import sys
# Use xrange wherever possible
try:
    range = xrange
except NameError:
    pass


def get_score(message):
    '''
    a function that takes input string and using letter 
    frequency it scores it. The closd the score is 
    to 1.00, the more realistic.
    '''
    score = 0
    freq = {'a': 0.0812, 'b': 0.0149, 'c': 0.0271, 'd': 0.0432,
    'e': 0.1202, 'f': 0.0230, 'g': 0.0202, 'h': 0.0592, 'i': 0.0731,
    'j': 0.001, 'k': 0.0069, 'l': 0.0398, 'm': 0.0261, 'n': 0.0695,
    'o': 0.0768, 'p': 0.0182, 'q': 0.0011, 'r': 0.0602, 's': 0.0628,
    't': 0.091, 'u': 0.0288, 'v': 0.0111, 'w': 0.0209, 'x': 0.0017,
    'y': 0.0211, 'z': 0.0007, ' ': .1}
    for c in message:
        score += freq.get(c, 0) #if it is not an alphabet, give it a score of 0
    return score/len(message)

result = []
for i in range(0, int(sys.argv[1])):
    with open("step1\\result_%d.txt" % (i), "r") as f:
        data = f.read(0x900)
        data=data.lower()  
        score = get_score(data)
        print(data[0:10])
        result.append([score, "result_%d" % i])
result.sort(key=lambda x:x[0], reverse=True)
print(result[0])
