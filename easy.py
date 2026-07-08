import math
def dot_product(v1, v2):
    if len(v1) != len(v2):
        raise ValueError("The length of the vectors don't match")
    result = 0
    for i in range(len(v1)):
        result += v1[i] * v2[i]
    return result


def magnitude(v):
    return math.sqrt(dot_product(v,v))
def angle_between(v1,v2):
    angle = dot_product(v1,v2)/(magnitude(v1)*magnitude (v2))
    cos = math.acos(angle)
    return cos
    
    




if __name__ == "__main__":
    res = dot_product([1, 2, 3], [4, 5, 6])
    print(res)
    assert res == 32
