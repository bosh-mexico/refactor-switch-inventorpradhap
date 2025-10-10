"""Tests for base payment processor"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, patch

from domain import PaymentMode, Money, PaymentRequest, PaymentStatus, InvalidAmountError
from infrastructure.processors.base import BasePaymentProcessor

class TestablePaymentProcessor(BasePaymentProcessor):
    """Testable implementation of base processor"""
    
    def _execute_payment(self, request):
        return "TEST_TXN_123"
    
    def supports_payment_mode(self, mode):
        return mode == PaymentMode.PAYPAL
    
    def get_supported_modes(self):
        return [PaymentMode.PAYPAL]
    
    def _get_processor_name(self):
        return "Test Processor"

class TestBasePaymentProcessor:
    """Test base payment processor"""
    
    @pytest.fixture
    def processor(self):
        """Processor fixture"""
        return TestablePaymentProcessor()
    
    @pytest.fixture
    def valid_request(self):
        """Valid payment request fixture"""
        return PaymentRequest(
            payment_mode=PaymentMode.PAYPAL,
            amount=Money(Decimal('100.00')),
        )
    
    def test_process_payment_success(self, processor, valid_request):
        """Test successful payment processing"""
        result = processor.process_payment(valid_request)
        
        assert result.status == PaymentStatus.SUCCESS
        assert result.transaction_id == "TEST_TXN_123"
        assert "Test Processor payment processed successfully" in result.message
    
    def test_process_payment_with_invalid_amount(self, processor):
        """Test payment processing with invalid amount"""
        request = PaymentRequest(
            payment_mode=PaymentMode.PAYPAL,
            amount=Money(Decimal('0.00')),
        )
        
        result = processor.process_payment(request)
        
        assert result.status == PaymentStatus.FAILED
        assert "Amount must be positive" in result.message
    
    def test_process_payment_with_amount_too_high(self, processor):
        """Test payment processing with amount too high"""
        request = PaymentRequest(
            payment_mode=PaymentMode.PAYPAL,
            amount=Money(Decimal('15000.00')),
        )
        
        result = processor.process_payment(request)
        
        assert result.status == PaymentStatus.FAILED
        assert "exceeds maximum limit" in result.message
    
    def test_validate_request_positive_amount(self, processor, valid_request):
        """Test request validation with positive amount"""
        # Should not raise exception
        processor._validate_request(valid_request)
    
    def test_validate_request_zero_amount(self, processor):
        """Test request validation with zero amount"""
        request = PaymentRequest(
            payment_mode=PaymentMode.PAYPAL,
            amount=Money(Decimal('0.00')),
        )
        
        with pytest.raises(InvalidAmountError, match="Amount must be positive"):
            processor._validate_request(request)
    
    def test_validate_request_amount_too_high(self, processor):
        """Test request validation with amount too high"""
        request = PaymentRequest(
            payment_mode=PaymentMode.PAYPAL,
            amount=Money(Decimal('15000.00')),
        )
        
        with pytest.raises(InvalidAmountError, match="exceeds maximum limit"):
            processor._validate_request(request)
    
    def test_generate_request_id(self, processor):
        """Test request ID generation"""
        request_id = processor._generate_request_id()
        
        assert isinstance(request_id, str)
        assert len(request_id) > 0
    
    def test_generate_transaction_id(self, processor, valid_request):
        """Test transaction ID generation"""
        transaction_id = processor._generate_transaction_id("TEST", valid_request)
        
        assert transaction_id.startswith("TEST_")
        assert len(transaction_id.split("_")) == 3  # PREFIX_HASH_UUID
    
    @patch('infrastructure.processors.base.BasePaymentProcessor._execute_payment')
    def test_process_payment_exception_handling(self, mock_execute, processor, valid_request):
        """Test exception handling in process_payment"""
        mock_execute.side_effect = Exception("Network error")
        
        result = processor.process_payment(valid_request)
        
        assert result.status == PaymentStatus.FAILED
        assert "Network error" in result.message