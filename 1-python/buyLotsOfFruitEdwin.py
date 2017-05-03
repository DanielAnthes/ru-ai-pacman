""" 
Edwin Wenink s4156072
Daniel Anthes s4767799
"""

fruitPrices = {'apples': 2.00, 'oranges': 1.50, 'pears': 1.75,
               'limes': 0.75, 'strawberries': 1.00}

def buyLotsOfFruit(orderList):
    """
        orderList: List of (fruit, numPounds) tuples
    Returns cost of order
    """
    totalPrice = 0

    for fruit, pounds in orderList:
        if fruit in fruitPrices:
            totalPrice = totalPrice + fruitPrices[fruit] * pounds
        else:
            return None

    return totalPrice

orderList = [('apples', 2), ('pears', 3), ('limes', 4), ('beer',5)]
print('Cost of', orderList, 'is', buyLotsOfFruit(orderList))

def quickSort (list):
    if len(list)==0 or len(list)==1:
        return list
    else:
        pivot = list.pop(0)
        return quickSort([x for x in list if x < pivot]) + [pivot] + quickSort([x for x in list if x >= pivot])

print(quickSort([4,6,5,4,3,6,43,2]))