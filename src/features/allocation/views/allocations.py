from sqlalchemy import text

from src.features.allocation.service_layer import unit_of_work


def allocations(orderid: str, uow: unit_of_work.SqlAlchemyUnitOfWork):
    with uow:
        results = uow.session.execute(
            text("SELECT sku, batchref FROM allocations_view WHERE orderid = :orderid"),
            dict(orderid=orderid),
        )
    return results
