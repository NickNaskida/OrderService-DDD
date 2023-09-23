from typing import List

from fastapi import APIRouter, HTTPException, status

from src.features.allocation import views
from src.features.allocation.api.schema import AllocationItem
from src.features.allocation.service_layer import unit_of_work


view_router = APIRouter()


@view_router.get("/allocations/{orderid}", status_code=200)
def allocations(orderid: str) -> List[AllocationItem]:
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    results = views.allocations(orderid, uow)

    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order {orderid} not found"
        )

    return results
