"""
Here's the intended output of this script, once you fill it in:

Welcome to shop1 fruit shop
Welcome to shop2 fruit shop
For orders:  [('apples', 1.0), ('oranges', 3.0)] best shop is shop1
For orders:  [('apples', 3.0)] best shop is shop2
"""

import shop

def shopSmart(orderList, fruitShops):
    """
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    """
    totalCosts = []

    for shop in fruitShops:
        price = shop.getPriceOfOrder(orderList)
        if price is not None:
            totalCosts.append((shop, price))

    if len(totalCosts) is not 0:
        cheapest = totalCosts.pop()
        while len(totalCosts)>0 :
            new = totalCosts.pop()
            if new[1] < cheapest[1]:
                cheapest = new
        return cheapest[0]

    else:
        return None




fruits1 = {'apples': 2.0, 'oranges':1.0}
fruits2 = {'apples': 1.0, 'oranges': 5.0}
shop1 =  shop.FruitShop('shop1',fruits1)
shop2 = shop.FruitShop('shop2',fruits2)
shops = [shop1, shop2]
orders1 = [('apples',1.0), ('oranges',3.0)]
orders2 = [('apples',3.0)]
print("For order", orders1, "the best shop is", shopSmart(orders1, shops).getName())
print("For order", orders2, "the best shop is", shopSmart(orders2, shops).getName())
