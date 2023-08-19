from abc import ABC, abstractmethod

from src.features.allocation.domain import model


class AbstractRepository(ABC):
    @abstractmethod
    def add(self, product: model.Product):
        raise NotImplementedError

    @abstractmethod
    def get(self, sku) -> model.Product:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, product):
        self.session.add(product)

    def get(self, sku):
        return self.session.query(model.Product).filter_by(sku=sku).first()
