from __future__ import annotations
from typing import Optional
from datetime import date

from src.features.allocation.domain import model
from src.features.allocation.domain.model import OrderLine
from src.features.allocation.service_layer import unit_of_work
from src.features.allocation.domain.exceptions import InvalidSku


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


def add_batch(
    ref: str, sku: str, qty: int, eta: Optional[date],
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        product = uow.products.get(sku=sku)
        if product is None:
            product = model.Product(sku, batches=[])
            uow.products.add(product)

        product.batches.append(model.Batch(ref, sku, qty, eta))
        uow.commit()


def allocate(
    orderid: str, sku: str, qty: int,
    uow: unit_of_work.AbstractUnitOfWork,
) -> str:
    line = OrderLine(orderid, sku, qty)
    with uow:
        product = uow.products.get(sku=line.sku)

        if product is None:
            raise InvalidSku(line.sku)
        batchref = product.allocate(line)
        uow.commit()
    return batchref
