"""Tests for PayPal processor"""
import pytest
from decimal import Decimal
from unittest.mock import patch

from domain import PaymentMode, Money, PaymentRequest, PaymentStatus
from infrastructure.processors.paypal import PayPalProcessor

class TestPayPalProcessor:
    """Test PayPal payment processor"""
    
    def test_supports_paypal_mode(self, paypal_processor):
        """Test that processor supports PayPal mode"""
        assert paypal_processor.supports_payment_mode(PaymentMode.PAYPAL) is True
        assert paypal_processor.supports_payment_mode(PaymentMode.GOOGLEPAY) is False
        assert paypal_processor.supports_payment_mode(PaymentMode.CREDITCARD) is False
    
    def test_get_supported_modes(self, paypal_processor):
        """Test getting supported modes"""
        modes = paypal_processor.get_supported_modes()
        
        assert modes == [PaymentMode.PAYPAL]
    
    def test_get_processor_name(self, paypal_processor):
        """Test getting processor name"""
        assert paypal_processor._get_processor_name() == "PayPal"
    
    @patch.object(PayPalProcessor, '_authenticate_paypal_account')
    @patch.object(PayPalProcessor, '_validate_paypal_payment')
    @patch.object(PayPalProcessor, '_submit_to_paypal')
    def test_execute_payment(self, mock_submit, mock_validate, mock_auth, paypal_processor):
        """Test PayPal payment execution"""
        request = PaymentRequest(
            payment_mode=PaymentMode.PAYPAL,
            amount=Money(Decimal('100.00')),
        )
        
        transaction_id = paypal_processor._execute_payment(request)
        
        # Verify PayPal-specific methods were called
        mock_auth.assert_called_once()
        mock_validate.assert_called_once_with(request)
        mock_submit.assert_called_once_with(request)
        
        # Verify transaction ID format
        assert transaction_id.startswith("PP_")
        assert len(transaction_id.split("_")) == 3
    
    def test_process_payment_success(self, paypal_processor):
        """Test successful PayPal payment processing"""
        request = PaymentRequest(
            payment_mode=PaymentMode.PAYPAL,
            amount=Money(Decimal('100.00')),
        )
        
        result = paypal_processor.process_payment(request)
        
        assert result.status == PaymentStatus.SUCCESS
        assert "PayPal payment" in result.message
        assert result.transaction_id.startswith("PP_")
    
    def test_authenticate_paypal_account(self, paypal_processor):
        """Test PayPal account authentication"""
        # Should not raise exception (placeholder implementation)
        paypal_processor._authenticate_paypal_account()
    
    def test_validate_paypal_payment(self, paypal_processor):
        """Test PayPal payment validation"""
        request = PaymentRequest(
            payment_mode=PaymentMode.PAYPAL,
            amount=Money(Decimal('100.00')),
        )
        # Should not raise exception (placeholder implementation)
        paypal_processor._validate_paypal_payment(request)
    
    def test_submit_to_paypal(self, paypal_processor):
        """Test PayPal submission"""
        request = PaymentRequest(
            payment_mode=PaymentMode.PAYPAL,
            amount=Money(Decimal('100.00')),
        )
        # Should not raise exception (placeholder implementation)
        paypal_processor._submit_to_paypal(request)