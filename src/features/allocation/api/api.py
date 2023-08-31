from datetime import datetime
from fastapi import APIRouter, HTTPException, status

from src.features.allocation.infrastructure import orm
from src.features.allocation.api.schema import BatchItem, OrderItem
from src.features.allocation.service_layer import services, unit_of_work
from src.features.allocation.domain.exceptions import InvalidSku, OutOfStock

api_router = APIRouter()
orm.start_mappers()


@api_router.post("/add_batch", status_code=status.HTTP_201_CREATED)
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


@api_router.post("/allocate", status_code=status.HTTP_201_CREATED)
def allocate_endpoint(item: OrderItem):
    try:
        batchref = services.allocate(
            item.orderid,
            item.sku,
            item.qty,
            unit_of_work.SqlAlchemyUnitOfWork(),
        )
    except (OutOfStock, InvalidSku) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return {"batchref": batchref}
