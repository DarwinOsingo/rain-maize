text = """
the cat sat on the mat
the cat ate the fish
the dog sat on the rug
the dog ate the bone
the dog chased the cat
the cat ran up the tree
a cat sat on the wall
a dog barked at the cat
the cat slept on the mat
the dog slept on the rug
a bird sang in the tree
the bird flew over the wall
the cat watched the bird
the dog watched the cat
a boy walked the dog
the boy fed the cat
the boy fed the dog
the cat drank the milk
the dog drank the water
a girl played with the cat
the girl played with the dog
"""
vocab = text.split()
lib = {}
for i in range(len(vocab)-1):
    current_word = vocab[i]
    next_word = vocab[i+1]
    if current_word not in lib:
        lib[current_word]={}
    if next_word not in lib[current_word]:
        lib[current_word][next_word]=1
    else:
        lib[current_word][next_word]+=1
prob={}
for x in lib:
    prob[x]={}
    total = sum(lib[x].values())
    for next_word,freq in lib[x].items():
        final = freq/total
        prob[x][next_word]=final
def generate(start_word,n):
    sentense = []
    if start_word not in prob:
        return(f'The word {start_word} isnt in our DB try again')
    sentense.append(start_word)
    while len(sentense)<n:
        after= prob[start_word]
        high = max(after,key=after.get)
        sentense.append(high)
        start_word=high
        
    return " ".join(sentense)
generate("the",7)
    

        


