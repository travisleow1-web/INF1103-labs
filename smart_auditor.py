
class Product:
    def __init__(self, product_id, name, price, stock):
        self._product_id = product_id
        self.name = name
        self._price = float(price)
        self._stock = int(stock)

    def update_stock(self, quantity):
        self._stock = quantity

    def display_information(self):
        print(f"ID: {self._product_id} | Name: {self.name} | Price: ${self._price:.2f} | Stock: {self._stock}")

    def to_dict(self):
        return {
            "product_id": self._product_id,
            "name": self.name,
            "price": self._price,
            "stock": self._stock
        }