from pydantic import BaseModel, Field


class BatchItem(BaseModel):
    ref: str = Field(..., example="batch-001")
    sku: str = Field(..., example="SMALL-TABLE")
    qty: int = Field(gt=0, description="The quantity must be greater than zero", example=20)
    eta: str = Field(..., example="2021-01-01")


class OrderItem(BaseModel):
    orderid: str = Field(..., example="order-001")
    sku: str = Field(..., example="SMALL-TABLE")
    qty: int = Field(gt=0, description="The quantity must be greater than zero", example=20)
