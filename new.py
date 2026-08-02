import random
class embeddings():
    def __init__(self,num_embeddings,embedding_dimesions):
        self.weight = [[random.uniform(-1,1) for _ in  range(num_embeddings)] for _ in range(embedding_dimesions)]
    
        pass