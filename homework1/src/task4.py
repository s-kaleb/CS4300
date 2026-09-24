#Calculating discount with any numeric price and discount

def calculate_discount(price, discount):
    
    finalPrice = 0.0
    finalPrice = price - (price *(discount / 100))
    print(finalPrice, end = "")