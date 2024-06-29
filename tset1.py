import pandas as pd
import random as r
import time as t
englishwords = pd.read_json("words_dictionary.json",typ="series")
englishwords = englishwords.keys()
englishwords = list(englishwords)
for i in range(len(englishwords)-1, -1, -1):
    if len(englishwords[i]) != 5:
        englishwords.pop(i)
print(len(englishwords))


r.seed(t.time() // 86400)
ranword = r.randint(0,15917)
print(englishwords[ranword])

a = 0
b = 0
word = englishwords[ranword]
guess = 'pousy'
word = list(str(word))
utext = list(str(guess))
for i in range(0,5):
        if word[i] == utext[i]:
            word[i] = '11'
            utext[i] = '1'
            print(i)
for j in range(0,5):
    for k in range(0,5):
        if word[j] == utext[k]:
            b += 1
            utext[k] = '2'
            word[j] = '22'
result = ''
for i in range(len(utext)):
    if utext[i] == '1':
        result += 'A'
    elif utext[i] == '2':
        result += 'B'
    else:
        result += 'C'
print(result)