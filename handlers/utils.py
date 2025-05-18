
def convert_price(price):
    price = str(price)[::-1]  # 850000 -> 000058
    temp = ''  # 0  00  000.058.
    count = 0  # 1  2   3   6
    for i in price:
        temp += i
        count += 1
        if count % 3 == 0:
            temp += '.'
    temp = temp[::-1]  # 000.058. -> .850.000
    if temp[0] == '.':  # 850.000
        return temp[1:]
    return temp
