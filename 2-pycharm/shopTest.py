import shop

aldiName = 'Aldi'
aldiPrices = {'apples': 1.00, 'oranges': 1.50, 'pears': 1.75}
aldiShop = shop.FruitShop(aldiName, aldiPrices)
aldiApples = aldiShop.getCostPerPound('apples')
print(aldiApples)
print('Apples cost %.2f at %s.' % (aldiApples, aldiName))

albertName = 'Albert Heijn'
albertPrices = {'kiwis':6.00, 'apples': 4.50, 'peaches': 8.75}
albertShop = shop.FruitShop(albertName, albertPrices)
albertApples = albertShop.getCostPerPound('apples')
print(albertApples)
print('Apples cost %.2f at %s.' % (albertApples, albertName))