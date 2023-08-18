"""Exceptions for the allocation domain."""


class OutOfStock(Exception):
    """OutOfStock exception is raised when there is no stock for a given SKU."""
    message = "Out of stock for sku {sku}"

    def __init__(self, sku: str):
        self.sku = sku

    def __str__(self):
        return self.message.format(sku=self.sku)


class InvalidSku(Exception):
    """Invalid sku exception is raised when a sku is not valid."""
    message = "Invalid sku {sku}"

    def __init__(self, sku: str):
        self.sku = sku

    def __str__(self):
        return self.message.format(sku=self.sku)
