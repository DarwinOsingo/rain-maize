numbers = [2, 7, 11, 15]
target = 9

for i in range(len(numbers)):
    for j in range(len(numbers)):
        if numbers[i] + numbers[j] == target:
            print([i, j])