from abc import ABC, abstractmethod

from src.services.product_parser.models.product_models import ProductsList


class BaseFromDTO(ABC):
    @abstractmethod
    def __call__(self) -> ProductsList:
        pass
