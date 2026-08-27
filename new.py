import random
text = """
the cat sat
the cat ate
the dog sat
the dog ate
"""
vocab= text.split()
count ={}
for i in range (len(vocab)-1):
    current_word = vocab[i]
    next_word = vocab[i+1]

    if current_word not in count:
        count[current_word]={}

    if next_word not in count[current_word]:
        count[current_word][next_word]=1
    else:
         count[current_word][next_word]+=1
probs = {}
for l in count:
    probs[l]={}
    total = sum(count[l].values())
    for next_word,freq in count[l].items():
        probs[l][next_word]=freq/total
def generate(start_word, n):
    sentense = []
    sentense.append(start_word)
    
            

            
    while n>0:
        if start_word not in probs or not probs[start_word]:
            print(f"'{start_word}' isn't present in this dataset")
            break
        after = probs[start_word]
       
        best = random.choices(list(after.keys()),weights= list(after.values()),k=1)[0]
      
       

        
        sentense.append(best)
        start_word=best
        n-=1
    return" ".join(sentense)

snet = generate("the",20)
print(snet)



    



    
    