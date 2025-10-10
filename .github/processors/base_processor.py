"""Base payment processor abstract class"""
from abc import ABC, abstractmethod
from enums import PaymentMode
from models import PaymentResult
from exceptions import InvalidAmountException

class PaymentProcessor(ABC):
    """Abstract base class for payment processors"""
    
    @abstractmethod
    def process_payment(self, amount: float) -> PaymentResult:
        """Process payment for the given amount"""
        pass
    
    @abstractmethod
    def get_payment_mode(self) -> PaymentMode:
        """Return the payment mode this processor handles"""
        pass
    
    def validate_amount(self, amount: float) -> None:
        """Validate payment amount"""
        if not isinstance(amount, (int, float)):
            raise InvalidAmountException("Amount must be a number")
        if amount <= 0:
            raise InvalidAmountException("Amount must be greater than zero")
        if amount > 10000:  # Example business rule
            raise InvalidAmountException("Amount exceeds maximum limit of $10,000")