"""Tests for Credit Card processor"""
import pytest
from decimal import Decimal
from unittest.mock import patch

from domain import PaymentMode, Money, PaymentRequest, PaymentStatus
from infrastructure.processors.creditcard import CreditCardProcessor

class TestCreditCardProcessor:
    """Test Credit Card payment processor"""
    
    def test_supports_creditcard_mode(self, creditcard_processor):
        """Test that processor supports Credit Card mode"""
        assert creditcard_processor.supports_payment_mode(PaymentMode.CREDITCARD) is True
        assert creditcard_processor.supports_payment_mode(PaymentMode.PAYPAL) is False
        assert creditcard_processor.supports_payment_mode(PaymentMode.GOOGLEPAY) is False
    
    def test_get_supported_modes(self, creditcard_processor):
        """Test getting supported modes"""
        modes = creditcard_processor.get_supported_modes()
        
        assert modes == [PaymentMode.CREDITCARD]
    
    def test_get_processor_name(self, creditcard_processor):
        """Test getting processor name"""
        assert creditcard_processor._get_processor_name() == "Credit Card"
    
    @patch.object(CreditCardProcessor, '_validate_card_details')
    @patch.object(CreditCardProcessor, '_run_fraud_detection')
    @patch.object(CreditCardProcessor, '_authorize_payment')
    @patch.object(CreditCardProcessor, '_capture_payment')
    def test_execute_payment(self, mock_capture, mock_authorize, mock_fraud, mock_validate, creditcard_processor):
        """Test Credit Card payment execution"""
        request = PaymentRequest(
            payment_mode=PaymentMode.CREDITCARD,
            amount=Money(Decimal('100.00')),
        )
        
        transaction_id = creditcard_processor._execute_payment(request)
        
        # Verify Credit Card-specific methods were called
        mock_validate.assert_called_once()
        mock_fraud.assert_called_once_with(request)
        mock_authorize.assert_called_once_with(request)
        mock_capture.assert_called_once_with(request)
        
        # Verify transaction ID format
        assert transaction_id.startswith("CC_")
        assert len(transaction_id.split("_")) == 3
    
    def test_process_payment_success(self, creditcard_processor):
        """Test successful Credit Card payment processing"""
        request = PaymentRequest(
            payment_mode=PaymentMode.CREDITCARD,
            amount=Money(Decimal('100.00')),
        )
        
        result = creditcard_processor.process_payment(request)
        
        assert result.status == PaymentStatus.SUCCESS
        assert "Credit Card payment" in result.message
        assert result.transaction_id.startswith("CC_")
    
    def test_validate_card_details(self, creditcard_processor):
        """Test card details validation"""
        # Should not raise exception (placeholder implementation)
        creditcard_processor._validate_card_details()
    
    def test_run_fraud_detection(self, creditcard_processor):
        """Test fraud detection"""
        request = PaymentRequest(
            payment_mode=PaymentMode.CREDITCARD,
            amount=Money(Decimal('100.00')),
        )
        # Should not raise exception (placeholder implementation)
        creditcard_processor._run_fraud_detection(request)
    
    def test_authorize_payment(self, creditcard_processor):
        """Test payment authorization"""
        request = PaymentRequest(
            payment_mode=PaymentMode.CREDITCARD,
            amount=Money(Decimal('100.00')),
        )
        # Should not raise exception (placeholder implementation)
        creditcard_processor._authorize_payment(request)
    
    def test_capture_payment(self, creditcard_processor):
        """Test payment capture"""
        request = PaymentRequest(
            payment_mode=PaymentMode.CREDITCARD,
            amount=Money(Decimal('100.00')),
        )
        # Should not raise exception (placeholder implementation)
        creditcard_processor._capture_payment(request)