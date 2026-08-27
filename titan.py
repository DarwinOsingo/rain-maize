text = """
he quick brown fox jumps over the lazy dog. Pack my box with five dozen liquor jugs!
"Where," she asked, "did you put the keys?" He replied: "I left them on the shelf."
Jinxed wizards pluck ivy from the big quilt; zebras march quickly, dodging trees.
It's a fine day (mostly) -- warm, bright, and calm. Don't you think so? I do.
Mr. Bloxby's cat, aged 12, ran 3 laps around the yard -- a new record!
"That's amazing," said Val; "we've never seen it move that fast."
Prices ranged from $5 to $99.99, depending on size & color.
"""
vocab = list(text)
words = sorted(list(set(vocab)))
words_to_ints = {ch:i for i,ch in enumerate(words)}
# for i,ch in enumerate( words):
#     if i not in words_to_ints:
#         words_to_ints[i]=ch
ints_to_words = {i:ch for i,ch in enumerate(words)}
# for i,ch in enumerate(words):
#     if i not in ints_to_words:
#         ints_to_words[i]=ch

encode = lambda s:[ words_to_ints[l] for l in s ]
decode = lambda t:"".join([ints_to_words[k]for k in t])
print(encode("boy"))
print(decode([16, 2, 17, 2, 12, 23, 18, 10, 18]))
#now I need to make x and y such that x +1 = y so that they correspond simple enough I could use a for loop 
#but im not sure what exactly to loop over 
data = encode(text)
x = data[:-1]
y=data[1:]
print(len(words))




