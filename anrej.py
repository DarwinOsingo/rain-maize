import torch 
with open("shakespere.txt","r")as f:
    text= f.read()
char = sorted(list(set(text)))

vocab = len(char)
#print(''.join(char))
stoi = {ch:i for i,ch in enumerate(char)}
itos = {i:ch for i,ch in enumerate (char)}
encode = lambda s:[stoi[c] for c in s]
decode = lambda d : ''.join([itos[i] for i in d])
print(encode("Hii there"))
print(decode(encode("Hii there")))
data = torch.tensor(encode(text),dtype=torch.long)
print(data.shape )
print(data[:100])
n = int(0.9*len(data))
train = data[:n]
val = data[n:]
block_size = 8
