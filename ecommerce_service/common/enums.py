from enum import Enum

class PaymentMethod(Enum):
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"
    PAYPAL = "PayPal"
    COD = "Cash on Delivery"

    @classmethod
    def choices(cls):
        return [(key.value, key.value) for key in cls]


class OrderStatus(Enum):
    PENDING = "Pending"
    PROCESSING = "Processing"
    COMPLETED = "Completed"

    @classmethod
    def choices(cls):
        return [(key.value, key.value) for key in cls]
