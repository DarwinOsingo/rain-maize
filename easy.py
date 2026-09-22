nums = [100, 4, 200, 1, 3, 2]
numbs =set(nums)
total = []
for num in numbs:
    
    if num -1 not in numbs and num + 1 in numbs:
        start = num
        total.append(num)
        while num + 1 in numbs:
            num +=1
            total.append(num)
    
print(total)
   