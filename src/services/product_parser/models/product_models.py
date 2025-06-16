from pydantic import BaseModel


class Product(BaseModel):
    link: str
    name: str
    price: float
    image: str = "images/placeholder.png"

    def __repr__(self) -> str:
        return f"Product(name={self.name}, price={self.price}, link={self.link}, image={self.image})"


class ProductsList(BaseModel):
    products: list[Product] = []

    def get_sorted_products(self) -> list[Product]:
        return sorted(self.products, key=lambda item: item.price)

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def del_product(self, index: int) -> None:
        self.products.pop(index)

    def __iter__(self) -> iter:
        return iter(self.products)

    def __len__(self) -> int:
        return len(self.products)

    def __getitem__(self, item):
        return self.products[item]

    def __repr__(self) -> str:
        return f"ProductList(products={self.products})"


class NamedProductsList:
    def __init__(self, name: str, products: ProductsList):
        self._name = name
        self._products = products

    @property
    def name(self) -> str:
        return self._name

    @property
    def products_list(self) -> ProductsList:
        return self._products

    @name.setter
    def name(self, value):
        self._name = value

    @products_list.setter
    def products_list(self, value):
        self._products = value


class ProductsListDTO:
    def __init__(self, *products: NamedProductsList) -> None:
        self.tuple_of_products = products

    def __call__(self) -> dict:
        output_json: dict = {}
        for marketplace, product_list in self.tuple_of_products:
            items: list = []
            for item in product_list.products:
                items.append(
                    {"image": item.image,
                     "link": item.link,
                     "name": item.name,
                     "price": item.price,}
                )
            output_json[marketplace]: dict[str] = items
        return output_json

    def __str__(self):
        return f"MarketPlaceList(list_of_products={self.tuple_of_products})"
