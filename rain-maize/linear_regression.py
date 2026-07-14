def attention(words):
    outputs = []
    for word in words:
        product = []
        for i in range(len(word)):
            sum += word[i]+word[i]
        # step 1: compute dot_product(word, w) for every w in words -> list of scores
        scores = []
        for w in words:
            pass  # fill in

        # step 2: turn scores into weights using softmax
        weights = []  # fill in

        # step 3: blend all words together using those weights
        # each word vector gets scaled by its weight, then summed element-wise
        blended = [0] * len(word)
        for weight, w in zip(weights, words):
            pass  # fill in: scale w by weight, add into blended

        outputs.append(blended)
    return outputs


if __name__ == "__main__":
    words = [
        [1, 0, 1],
        [0, 1, 1],
        [1, 1, 0],
    ]
    result = attention(words)
    for i, out in enumerate(result):
        print(f"word {i}: {out}")