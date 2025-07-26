def caesar_cipher(m,s,e=True):
    r= ""
    s=s% 26
    if not e:
        s= -s
    for i in m:
        if i.isalpha():
            base = ord('A') if i.isupper() else ord('a')
            r += chr((ord(i) - base + s) % 26 + base)
        else:
            r+=i
    return r
m=input()
s=int(input())
e=input()
print(caesar_cipher(m,s,e))
