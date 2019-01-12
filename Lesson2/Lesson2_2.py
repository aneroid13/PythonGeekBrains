import json
import datetime
import inspect


item = "SpeicalItem"
quantity = 4
price = "10c"
buyer = "Mr. Somebody"
date = str(datetime.datetime.now())


def write_order_to_json(item, quantity, price, buyer, date):
    with open('orders.json', encoding='utf-8') as f_n:
        orders = json.load(f_n)

    onebuy = {
        "item": item,
        "quantity": quantity,
        "price": price,
        "buyer": buyer,
        "date": date
        }

    orders.get("orders").append(onebuy)

    with open('orders.json', 'w') as f_n:
        json.dump(orders, f_n, indent=4)


write_order_to_json(item, quantity, price, buyer, date)
