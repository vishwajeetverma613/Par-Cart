from enum import Enum

class PaymentMethod(Enum):
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"
    PAYPAL = "PayPal"
    COD = "Cash on Delivery"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class OrderStatus(Enum):
    PENDING = "Pending"
    RECIEVED = "Recieved"
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELED = "Canceled"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
