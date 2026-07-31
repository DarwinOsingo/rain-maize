import random

class RawEmbedding:
    def __init__(self, num_embeddings, embedding_dim):
        # Create a 2D list (matrix) filled with random float numbers
        # Shape: [num_embeddings x embedding_dim]
        self.weight = [
            [random.uniform(-1, 1) for _ in range(embedding_dim)]
            for _ in range(num_embeddings)
        ]

    def forward(self, idx):
        # idx is a 2D list of shape [Batch, Sequence_Length]
        # We loop through every token ID and fetch its corresponding vector (row) from self.weight
        output = []
        for batch in idx:
            batch_vectors = []
            for token_id in batch:
                # Direct row lookup in our list table
                vector = self.weight[token_id]
                batch_vectors.append(vector)
            output.append(batch_vectors)
            
        return output

# --- Testing it out ---
vocab_size = 65
embedding_dim = 32

# Instantiate
my_embed = RawEmbedding(vocab_size, embedding_dim)

# Input: Batch of 2 sentences, 4 token IDs each
idx = [
    [1, 5, 23, 64],
    [0, 12, 5, 3]
]

output = my_embed.forward(idx)

# Verify the dimensions manually
batch_size = len(output)
seq_len = len(output[0])
vector_dim = len(output[0][0])

print(f"Output dimensions: [{batch_size}, {seq_len}, {vector_dim}]")
# Output dimensions: [2, 4, 32]