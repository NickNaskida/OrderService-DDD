from datetime import date

from pydantic import model_validator

from src.features.allocation import views
from src.features.allocation.domain import commands
from src.features.allocation.service_layer import unit_of_work, messagebus

today = date.today()


def test_allocations_view(sqlite_session_factory):
    uow = unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory)
    messagebus.handle(commands.CreateBatch("sku1batch", "sku1", 50, None), uow)
    messagebus.handle(commands.CreateBatch("sku2batch", "sku2", 50, today), uow)
    messagebus.handle(commands.Allocate("order1", "sku1", 20), uow)
    messagebus.handle(commands.Allocate("order1", "sku2", 20), uow)
    # add a spurious batch and order to make sure we're getting the right ones
    messagebus.handle(commands.CreateBatch("sku1batch-later", "sku1", 50, today), uow)
    messagebus.handle(commands.Allocate("otherorder", "sku1", 30), uow)
    messagebus.handle(commands.Allocate("otherorder", "sku2", 10), uow)

    result = views.allocations("order1", uow)

    order_objects = [dict(r._mapping) for r in result]

    assert order_objects == [
        {"sku": "sku1", "batchref": "sku1batch"},
        {"sku": "sku2", "batchref": "sku2batch"},
    ]




