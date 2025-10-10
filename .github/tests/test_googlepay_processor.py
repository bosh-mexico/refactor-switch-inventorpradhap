"""Tests for Google Pay processor"""
import pytest
from decimal import Decimal
from unittest.mock import patch

from domain import PaymentMode, Money, PaymentRequest, PaymentStatus
from infrastructure.processors.googlepay import GooglePayProcessor

class TestGooglePayProcessor:
    """Test Google Pay payment processor"""
    
    def test_supports_googlepay_mode(self, googlepay_processor):
        """Test that processor supports Google Pay mode"""
        assert googlepay_processor.supports_payment_mode(PaymentMode.GOOGLEPAY) is True
        assert googlepay_processor.supports_payment_mode(PaymentMode.PAYPAL) is False
        assert googlepay_processor.supports_payment_mode(PaymentMode.CREDITCARD) is False
    
    def test_get_supported_modes(self, googlepay_processor):
        """Test getting supported modes"""
        modes = googlepay_processor.get_supported_modes()
        
        assert modes == [PaymentMode.GOOGLEPAY]
    
    def test_get_processor_name(self, googlepay_processor):
        """Test getting processor name"""
        assert googlepay_processor._get_processor_name() == "Google Pay"
    
    @patch.object(GooglePayProcessor, '_verify_google_token')
    @patch.object(GooglePayProcessor, '_validate_google_payment')
    @patch.object(GooglePayProcessor, '_process_with_google')
    def test_execute_payment(self, mock_process, mock_validate, mock_verify, googlepay_processor):
        """Test Google Pay payment execution"""
        request = PaymentRequest(
            payment_mode=PaymentMode.GOOGLEPAY,
            amount=Money(Decimal('100.00')),
        )
        
        transaction_id = googlepay_processor._execute_payment(request)
        
        # Verify Google Pay-specific methods were called
        mock_verify.assert_called_once()
        mock_validate.assert_called_once_with(request)
        mock_process.assert_called_once_with(request)
        
        # Verify transaction ID format
        assert transaction_id.startswith("GP_")
        assert len(transaction_id.split("_")) == 3
    
    def test_process_payment_success(self, googlepay_processor):
        """Test successful Google Pay payment processing"""
        request = PaymentRequest(
            payment_mode=PaymentMode.GOOGLEPAY,
            amount=Money(Decimal('100.00')),
        )
        
        result = googlepay_processor.process_payment(request)
        
        assert result.status == PaymentStatus.SUCCESS
        assert "GooglePay payment" in result.message
        assert result.transaction_id.startswith("GP_")
    
    def test_verify_google_token(self, googlepay_processor):
        """Test Google Pay token verification"""
        # Should not raise exception (placeholder implementation)
        googlepay_processor._verify_google_token()
    
    def test_validate_google_payment(self, googlepay_processor):
        """Test Google Pay payment validation"""
        request = PaymentRequest(
            payment_mode=PaymentMode.GOOGLEPAY,
            amount=Money(Decimal('100.00')),
        )
        # Should not raise exception (placeholder implementation)
        googlepay_processor._validate_google_payment(request)
    
    def test_process_with_google(self, googlepay_processor):
        """Test Google Pay processing"""
        request = PaymentRequest(
            payment_mode=PaymentMode.GOOGLEPAY,
            amount=Money(Decimal('100.00')),
        )
        # Should not raise exception (placeholder implementation)
        googlepay_processor._process_with_google(request)