"""Custom exceptions for payment processing"""

class PaymentException(Exception):
    """Base exception for payment-related errors"""
    pass

class InvalidPaymentModeException(PaymentException):
    """Exception raised for invalid payment modes"""
    pass

class InvalidAmountException(PaymentException):
    """Exception raised for invalid payment amounts"""
    pass

class PaymentProcessingException(PaymentException):
    """Exception raised when payment processing fails"""
    pass