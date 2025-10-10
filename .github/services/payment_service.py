"""Main payment service"""
from enums import PaymentMode
from models import PaymentResult
from services.payment_factory import PaymentProcessorFactory
from exceptions import PaymentException, InvalidPaymentModeException
from utils import setup_logger
from typing import List

logger = setup_logger(__name__)

class PaymentService:
    """Main service class for handling payments"""
    
    def __init__(self):
        self.factory = PaymentProcessorFactory()
    
    def checkout(self, mode: PaymentMode, amount: float) -> PaymentResult:
        """
        Process checkout with given payment mode and amount
        
        Args:
            mode: Payment mode enum
            amount: Payment amount
            
        Returns:
            PaymentResult object with processing details
            
        Raises:
            PaymentException: For various payment-related errors
        """
        try:
            # Validate input parameters
            if not isinstance(mode, PaymentMode):
                raise InvalidPaymentModeException("Invalid payment mode provided")
            
            # Create appropriate processor
            processor = self.factory.create_processor(mode)
            
            # Process payment
            result = processor.process_payment(amount)
            
            if result.success:
                logger.info(f"Payment processed successfully: {result.message}")
            else:
                logger.warning(f"Payment processing failed: {result.message}")
            
            return result
            
        except PaymentException as e:
            error_msg = f"Payment processing failed: {str(e)}"
            logger.error(error_msg)
            return PaymentResult(success=False, message=error_msg)
        
        except Exception as e:
            error_msg = f"Unexpected error during payment processing: {str(e)}"
            logger.error(error_msg)
            return PaymentResult(success=False, message="Payment processing failed due to system error")
    
    def get_supported_payment_modes(self) -> List[PaymentMode]:
        """Return list of supported payment modes"""
        return self.factory.get_supported_modes()
    
    def is_payment_mode_supported(self, mode: PaymentMode) -> bool:
        """Check if payment mode is supported"""
        return self.factory.is_supported_mode(mode)