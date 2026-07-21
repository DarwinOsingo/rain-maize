import torch 
with open("shadow-slave/shadow-slave/0001 - Chapter 1 Nightmare Begins.txt","r") as f:
    text = f.read()
char = sorted(list(set(text)))
stoi = {ch:i for i,ch in enumerate(char)}
itos = {i:ch for i,ch in enumerate(char)}
encode = lambda s:[stoi[c] for c in s ]
decode = lambda d : "".join(itos[c] for c in d)
print(encode("Helo"))
print(decode([19, 39, 46, 49]))
def stoi():
    stoi ={}
    for i,ch in enumerate(char):
        stoi[ch] = i