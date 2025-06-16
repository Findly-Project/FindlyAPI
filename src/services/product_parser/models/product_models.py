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


class MarketPlaceList:
    def __init__(self) -> None:
        self.list_of_products: dict = {}

    def add_list_of_products(self, list_name: str, list_data: ProductsList) -> None:
        self.list_of_products[list_name]: ProductsList = list_data

    def get_json(self) -> dict:
        output_json: dict = {}
        for marketplace, product_list in self.list_of_products.items():
            items: list = []
            for item in product_list.products:
                items.append(
                    {
                        "image": item.image,
                        "link": item.link,
                        "name": item.name,
                        "price": item.price,
                    }
                )
            output_json[marketplace]: dict[str] = items
        return output_json

    def __str__(self):
        return f"MarketPlaceList(list_of_products={self.list_of_products})"
