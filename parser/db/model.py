

class Store:
    def __init__(self, name: str, code:str, id:int=None) -> None:
        self.id = id
        self.name = name
        self.code = code


class Product:
    def __init__(self, product_id:int, store_id:int, name:str, code:str, category:str, category_code:str, price:float, id:int=None) -> None:
        self.id = id
        self.name = name
        self.code = code
        self.product_id = product_id
        self.store_id = store_id
        self.category = category
        self.category_code = category_code
        self.price = price
