from datetime import datetime
from fastapi import APIRouter, HTTPException, status

from src.features.allocation.domain import commands
from src.features.allocation.api.views import view_router
from src.features.allocation.api.schema import BatchItem, OrderItem
from src.features.allocation.service_layer import messagebus, unit_of_work
from src.features.allocation.domain.exceptions import InvalidSku, OutOfStock

api_router = APIRouter()
api_router.include_router(view_router)


@api_router.post("/add_batch", status_code=status.HTTP_201_CREATED)
def add_batch(item: BatchItem):
    eta = item.eta

    if eta is not None:
        eta = datetime.fromisoformat(eta).date()

    cmd = commands.CreateBatch(item.ref, item.sku, item.qty, eta)
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    messagebus.handle(cmd, uow)
    return "OK"


@api_router.post("/allocate", status_code=status.HTTP_201_CREATED)
def allocate_endpoint(item: OrderItem):
    try:
        cmd = commands.Allocate(item.orderid, item.sku, item.qty)
        uow = unit_of_work.SqlAlchemyUnitOfWork()
        results = messagebus.handle(cmd, uow)
        batchref = results.pop()
    except (InvalidSku, OutOfStock) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return {"batchref": batchref}
