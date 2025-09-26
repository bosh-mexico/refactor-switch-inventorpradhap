from enum import Enum

class PaymentMode(Enum):
    """
    Enum representing supported payment modes
    """
    PAYPAL = 1
    GOOGLEPAY = 2
    CREDITCARD = 3
    UNKNOWN = 99
    
    @classmethod
    def is_valid(cls, mode):
        """
        Check if the payment mode is valid (supported)
        """
        return mode in [cls.PAYPAL, cls.GOOGLEPAY, cls.CREDITCARD]
    
    @classmethod
    def get_supported_modes(cls):
        """
        Get list of supported payment modes
        """
        return [cls.PAYPAL, cls.GOOGLEPAY, cls.CREDITCARD]