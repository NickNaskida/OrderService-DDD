from datetime import datetime
from http import HTTPStatus
from fastapi import FastAPI, HTTPException

from src.features.allocation.infrastructure import orm
from src.features.allocation.api.schema import BatchItem, OrderItem
from src.features.allocation.service_layer import services, unit_of_work
from src.features.allocation.domain.exceptions import InvalidSku, OutOfStock

app = FastAPI()
orm.start_mappers()


@app.post("/add_batch", status_code=HTTPStatus.CREATED)
def add_batch(item: BatchItem):
    eta = item.eta

    if eta is not None:
        eta = datetime.fromisoformat(eta).date()

    services.add_batch(
        item.ref,
        item.sku,
        item.qty,
        eta,
        unit_of_work.SqlAlchemyUnitOfWork()
    )
    return "OK"


@app.post("/allocate", status_code=HTTPStatus.CREATED)
def allocate_endpoint(item: OrderItem):
    try:
        batchref = services.allocate(
            item.orderid,
            item.sku,
            item.qty,
            unit_of_work.SqlAlchemyUnitOfWork(),
        )
    except (OutOfStock, InvalidSku) as e:
        return HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=str(e)
        )

    return {"batchref": batchref}
