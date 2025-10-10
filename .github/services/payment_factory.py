"""Payment processor factory"""
from typing import Dict, Type, List
from enums import PaymentMode
from processors import PaymentProcessor, PayPalProcessor, GooglePayProcessor, CreditCardProcessor
from exceptions import InvalidPaymentModeException

class PaymentProcessorFactory:
    """Factory class to create payment processors"""
    
    _processors: Dict[PaymentMode, Type[PaymentProcessor]] = {
        PaymentMode.PAYPAL: PayPalProcessor,
        PaymentMode.GOOGLEPAY: GooglePayProcessor,
        PaymentMode.CREDITCARD: CreditCardProcessor,
    }
    
    @classmethod
    def create_processor(cls, mode: PaymentMode) -> PaymentProcessor:
        """Create and return appropriate payment processor"""
        if mode not in cls._processors:
            raise InvalidPaymentModeException(f"Unsupported payment mode: {mode}")
        
        processor_class = cls._processors[mode]
        return processor_class()
    
    @classmethod
    def register_processor(cls, mode: PaymentMode, processor_class: Type[PaymentProcessor]):
        """Register a new payment processor (for extensibility)"""
        cls._processors[mode] = processor_class
    
    @classmethod
    def get_supported_modes(cls) -> List[PaymentMode]:
        """Return list of supported payment modes"""
        return list(cls._processors.keys())
    
    @classmethod
    def is_supported_mode(cls, mode: PaymentMode) -> bool:
        """Check if payment mode is supported"""
        return mode in cls._processors