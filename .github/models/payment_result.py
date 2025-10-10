"""Payment result model"""
from typing import Optional

class PaymentResult:
    """Data class to represent payment processing result"""
    
    def __init__(self, success: bool, message: str, transaction_id: Optional[str] = None):
        self.success = success
        self.message = message
        self.transaction_id = transaction_id
    
    def __str__(self) -> str:
        return f"PaymentResult(success={self.success}, message='{self.message}', transaction_id='{self.transaction_id}')"
    
    def __repr__(self) -> str:
        return self.__str__()