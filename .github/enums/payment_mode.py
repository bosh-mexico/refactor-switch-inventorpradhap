"""Payment mode enumeration"""
from enum import Enum

class PaymentMode(Enum):
    """Enum for supported payment modes"""
    PAYPAL = "paypal"
    GOOGLEPAY = "googlepay"
    CREDITCARD = "creditcard"