nums = [3, -2, 1, 0, -1, 2, -3, 4]
target = 2
nums.sort()
pairs =[]
for i in range(len(nums)):
    left = i+1
    right = len(nums)-1
    while left < right:
        total = nums[i]+nums[left]+nums[right]
        if total == target:
            pairs.append([nums[right],nums[left],nums[i]])
        elif total > target:
            right -=1
        else:
            left+=1
print(pairs)


