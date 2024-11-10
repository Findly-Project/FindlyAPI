from typing import List, Any, Dict


class ProductData:
    default_image_url: str = "images/placeholder.png"

    def __init__(
        self, link: str, name: str, price: float, image: str | None = default_image_url
    ) -> None:
        self.link: str = link
        self.name: str = name
        self.image: str = image
        self.price: float = price

    def __repr__(self) -> str:
        return f"ProductData(name={self.name}, price={self.price}, link={self.link})"


class ProductList:
    def __init__(self, products: List[ProductData] | None = None) -> None:
        self.products: List[ProductData] = products if products else []

    def add_product(self, product: ProductData) -> None:
        self.products.append(product)

    def del_product(self, index: int) -> None:
        self.products.pop(index)

    def __iter__(self) -> iter:
        return iter(self.products)

    def __len__(self) -> int:
        return len(self.products)

    def __getitem__(self, item) -> Any:
        return self.products[item]

    def __repr__(self) -> str:
        return f"ProductList(products={self.products})"


class SortAndFilterProductList:
    @staticmethod
    def filter_by_name(names: List[str], products: ProductList) -> ProductList:
        products_list: List[ProductData] = [
            item for item in products if item.name in names
        ]
        return ProductList(products_list)

    @staticmethod
    def sort_by_price(products: ProductList) -> ProductList:
        return ProductList(
            sorted([item for item in products.products], key=lambda c: c.price)
        )


class MarketPlaceList:
    def __init__(self) -> None:
        self.list_of_products: Dict = {}

    def add_list_of_products(self, list_name: str, list_data: ProductList) -> None:
        self.list_of_products[list_name]: ProductList = list_data

    def get_json(self) -> Dict:
        output_json: Dict[str] = {}
        for marketplace, product_list in self.list_of_products.items():
            items: List = []
            for item in product_list.products:
                items.append(
                    {
                        "image": item.image,
                        "link": item.link,
                        "name": item.name,
                        "price": item.price,
                    }
                )
            output_json[marketplace] = items
        return output_json
