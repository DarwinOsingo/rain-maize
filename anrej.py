import torch 
import torch.nn as nn
import torch.nn.functional as f

with open("shakespere.txt","r")as file:
    text= file.read()
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


n = int(0.9*len(data))
train = data[:n]
val = data[n:]

block_size = 8
batch_size = 4
train[:block_size+1]
x = train[:block_size]
y = train[1:block_size+1]

torch.manual_seed(42)
def get_batches(split):
    data = train if split == "train" else val
    ix = torch.randint(0,len(data)-block_size,(batch_size,))
    x = torch.stack([data[i:block_size+i] for i in ix])
    y = torch.stack([data[i+1:i+block_size+1] for i in ix])
    return x,y
xb,yb = get_batches("train")
print(xb.shape)
print(yb.shape)
for b in range(batch_size):
    for t in range (block_size):
        context = xb[b,:t+1]
        target = yb[b,t]
        print(f"if context is {context} then the prediction should be {target}")
class BigramLanguageModel(nn.Module):
    def __init__(self,vocab_size):
        super().__init__()
        self.token_lookup_table = nn.Embedding(vocab_size,vocab_size)
    def forward(self,idx,targets=None):
        logits = self.token_lookup_table(idx)
        if targets == None:
            loss = None
        
    

    


