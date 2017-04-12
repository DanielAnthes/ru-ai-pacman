nums = [1,2,3,4,5,6]
oddNums = [x for x in nums if x % 2 == 1]
print (oddNums)
oddNumsPlusOne=[x+1 for x in nums if x% 2 == 1]
print(oddNumsPlusOne)

strings = ["Beer", "LaTrappe", "Chival", "Westmalle", "Heinekeken"]
longStr = [str.lower() for str in strings if len(str)>5]
print(longStr)