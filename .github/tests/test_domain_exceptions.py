"""Tests for domain exceptions"""
import pytest
from domain import (
    PaymentDomainException,
    InvalidPaymentModeError,
    InvalidAmountError,
    PaymentProcessingError,
    UnsupportedOperationError
)

class TestPaymentDomainException:
    """Test base domain exception"""
    
    def test_payment_domain_exception_creation(self):
        """Test creating payment domain exception"""
        exception = PaymentDomainException("Test message", "TEST_ERROR")
        
        assert str(exception) == "Test message"
        assert exception.message == "Test message"
        assert exception.error_code == "TEST_ERROR"
    
    def test_payment_domain_exception_without_error_code(self):
        """Test creating exception without error code"""
        exception = PaymentDomainException("Test message")
        
        assert exception.error_code is None

class TestInvalidPaymentModeError:
    """Test invalid payment mode error"""
    
    def test_invalid_payment_mode_error(self):
        """Test invalid payment mode error"""
        error = InvalidPaymentModeError("invalid_mode")
        
        assert "Invalid payment mode: invalid_mode" in str(error)
        assert error.error_code == "INVALID_PAYMENT_MODE"

class TestInvalidAmountError:
    """Test invalid amount error"""
    
    def test_invalid_amount_error(self):
        """Test invalid amount error"""
        error = InvalidAmountError(100.0, "Amount too high")
        
        assert "Invalid amount 100.0: Amount too high" in str(error)
        assert error.error_code == "INVALID_AMOUNT"

class TestPaymentProcessingError:
    """Test payment processing error"""
    
    def test_payment_processing_error(self):
        """Test payment processing error"""
        error = PaymentProcessingError("Network timeout")
        
        assert "Payment processing failed: Network timeout" in str(error)
        assert error.error_code == "PROCESSING_ERROR"

class TestUnsupportedOperationError:
    """Test unsupported operation error"""
    
    def test_unsupported_operation_error(self):
        """Test unsupported operation error"""
        error = UnsupportedOperationError("refund", "PayPal")
        
        assert "Operation refund not supported by PayPal" in str(error)
        assert error.error_code == "UNSUPPORTED_OPERATION"