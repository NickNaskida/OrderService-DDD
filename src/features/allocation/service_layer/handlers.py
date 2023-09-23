from __future__ import annotations
from typing import TYPE_CHECKING
from dataclasses import asdict

from sqlalchemy import text

from src.features.allocation.infrastructure import email
from src.features.allocation.domain import commands, events, model
from src.features.allocation.domain.model import OrderLine
from src.features.allocation.domain.exceptions import InvalidSku

if TYPE_CHECKING:
    from . import unit_of_work


def add_batch(
    cmd: commands.CreateBatch,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        product = uow.products.get(sku=cmd.sku)
        if product is None:
            product = model.Product(cmd.sku, batches=[])
            uow.products.add(product)
        product.batches.append(model.Batch(cmd.ref, cmd.sku, cmd.qty, cmd.eta))
        uow.commit()


def allocate(
    cmd: commands.Allocate,
    uow: unit_of_work.AbstractUnitOfWork,
) -> str:
    line = OrderLine(cmd.orderid, cmd.sku, cmd.qty)
    with uow:
        product = uow.products.get(sku=line.sku)
        if product is None:
            raise InvalidSku(line.sku)
        batchref = product.allocate(line)
        uow.commit()
        return batchref


def reallocate(
    event: events.Deallocated,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        product = uow.products.get(sku=event.sku)
        product.events.append(commands.Allocate(**asdict(event)))
        uow.commit()


def change_batch_quantity(
    cmd: commands.ChangeBatchQuantity,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        product = uow.products.get_by_batchref(batchref=cmd.ref)
        product.change_batch_quantity(ref=cmd.ref, qty=cmd.qty)
        uow.commit()


def send_out_of_stock_notification(
    event: events.OutOfStock,
    uow: unit_of_work.AbstractUnitOfWork,
):
    # TODO: append message to RabbitMQ and handle it with seperate microservice
    email.send(
        "stock@made.com",
        f"Out of stock for {event.sku}",
    )


def add_allocation_to_read_model(
    event: events.Allocated,
    uow: unit_of_work.SqlAlchemyUnitOfWork,
):
    with uow:
        uow.session.execute(
            text("""
            INSERT INTO allocations_view (orderid, sku, batchref)
            VALUES (:orderid, :sku, :batchref)
            """),
            dict(orderid=event.orderid, sku=event.sku, batchref=event.batchref),
        )
        uow.commit()


def remove_allocation_from_read_model(
    event: events.Deallocated,
    uow: unit_of_work.SqlAlchemyUnitOfWork,
):
    with uow:
        uow.session.execute(
            text("""
            DELETE FROM allocations_view
            WHERE orderid = :orderid AND sku = :sku
            """),
            dict(orderid=event.orderid, sku=event.sku),
        )
        uow.commit()
