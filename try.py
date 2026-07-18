import torch
data =torch.tensor([i for i in range(1,1001)],dtype=torch.long)
context = 12

ix = torch.randint(len(data)-context,(4,))
x = torch.stack([data[i:context+i] for i in ix])
y = torch.stack([data[i+1:context+1+i] for i in ix])
print(x)
print(y)