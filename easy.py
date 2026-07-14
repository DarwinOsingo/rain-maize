# Current assignment: matrix_vector_multiply — take a matrix (a list of row-vectors) and multiply it by a vector.'
#  Each row of the matrix gets dot-producted with the vector, and you collect those results into a new output vector.
# you already have a function that takes two vectors and returns a single number — that's exactly what you need inside the loop, applied to each row against vector.
# Why this matters: this operation is literally what a neural network layer (nn.Linear) does under the hood — it's one step closer to real attention,
#  which needs matrix multiplication to transform word vectors into Queries, Keys, and Values.

import math

def dot_product(v1, v2):
    if len(v1) != len(v2):
        raise ValueError("The length of the vectors don't match")
    result = 0
    for i in range(len(v1)):
        result += v1[i] * v2[i]
    return result


def magnitude(v):
    return math.sqrt(dot_product(v, v))


def angle_between(v1, v2):
    angle = dot_product(v1, v2) / (magnitude(v1) * magnitude(v2))
    cos = math.acos(angle)
    return cos


def matrix_vector_multiply(matrix, vector):
    result = []
    for row in matrix:
        if len(row) != len(vector):
            raise ValueError("The number of matrixes should mirror the number of vectors!!")
        answer = dot_product(row,vector)
        result.append(answer)
    return result
def softmax(scores):
    result = []
    # step 1: exponentiate every value in `scores`
    # step 2: sum up all those exponentiated values
    # step 3: divide each exponentiated value by that sum
    # step 4: collect into result
    answer = [math.exp(x) for x in scores]
    total = sum(answer)
    result =[exp/total for exp in answer]
    return result


if __name__ == "__main__":
    res = softmax([1, 2, 3])
    print(res)
    assert math.isclose(sum(res), 1.0)