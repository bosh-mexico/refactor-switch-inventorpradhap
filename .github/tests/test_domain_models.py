"""Tests for domain models"""
import pytest
from decimal import Decimal
from datetime import datetime

from domain import Money, PaymentRequest, PaymentResult, PaymentMode, PaymentStatus, TransactionType

class TestMoney:
    """Test Money value object"""
    
    def test_money_creation_with_valid_amount(self):
        """Test creating money with valid amount"""
        money = Money(amount=Decimal('100.50'), currency='USD')
        
        assert money.amount == Decimal('100.50')
        assert money.currency == 'USD'
    
    def test_money_creation_with_default_currency(self):
        """Test creating money with default currency"""
        money = Money(amount=Decimal('100.00'))
        
        assert money.currency == 'USD'
    
    def test_money_negative_amount_raises_error(self):
        """Test that negative amount raises error"""
        with pytest.raises(ValueError, match="Amount cannot be negative"):
            Money(amount=Decimal('-100.00'))
    
    def test_money_empty_currency_raises_error(self):
        """Test that empty currency raises error"""
        with pytest.raises(ValueError, match="Currency is required"):
            Money(amount=Decimal('100.00'), currency='')
    
    def test_money_string_representation(self):
        """Test money string representation"""
        money = Money(amount=Decimal('100.50'), currency='EUR')
        
        assert str(money) == 'EUR 100.50'
    
    def test_money_immutability(self):
        """Test that money is immutable"""
        money = Money(amount=Decimal('100.00'))
        
        with pytest.raises(AttributeError):
            money.amount = Decimal('200.00')

class TestPaymentRequest:
    """Test PaymentRequest value object"""
    
    def test_payment_request_creation(self, sample_money):
        """Test creating payment request"""
        request = PaymentRequest(
            payment_mode=PaymentMode.PAYPAL,
            amount=sample_money,
            transaction_type=TransactionType.PURCHASE
        )
        
        assert request.payment_mode == PaymentMode.PAYPAL
        assert request.amount == sample_money
        assert request.transaction_type == TransactionType.PURCHASE
        assert request.metadata is None
    
    def test_payment_request_with_metadata(self, sample_money):
        """Test creating payment request with metadata"""
        metadata = {"user_id": "123", "order_id": "ORD-456"}
        request = PaymentRequest(
            payment_mode=PaymentMode.GOOGLEPAY,
            amount=sample_money,
            metadata=metadata
        )
        
        assert request.metadata == metadata
    
    def test_payment_request_invalid_payment_mode(self, sample_money):
        """Test payment request with invalid payment mode"""
        with pytest.raises(ValueError, match="Invalid payment mode"):
            PaymentRequest(
                payment_mode="invalid_mode",  # type: ignore
                amount=sample_money
            )
    
    def test_payment_request_immutability(self, sample_payment_request):
        """Test that payment request is immutable"""
        with pytest.raises(AttributeError):
            sample_payment_request.payment_mode = PaymentMode.CREDITCARD

class TestPaymentResult:
    """Test PaymentResult model"""
    
    def test_payment_result_creation(self):
        """Test creating payment result"""
        result = PaymentResult(
            request_id="REQ-123",
            status=PaymentStatus.SUCCESS,
            message="Payment successful",
            transaction_id="TXN-456"
        )
        
        assert result.request_id == "REQ-123"
        assert result.status == PaymentStatus.SUCCESS
        assert result.message == "Payment successful"
        assert result.transaction_id == "TXN-456"
    
    def test_payment_result_success_factory(self):
        """Test success factory method"""
        result = PaymentResult.success(
            request_id="REQ-123",
            transaction_id="TXN-456",
            message="Custom success message"
        )
        
        assert result.status == PaymentStatus.SUCCESS
        assert result.transaction_id == "TXN-456"
        assert result.message == "Custom success message"
        assert result.processed_at is not None
        assert result.is_successful is True
    
    def test_payment_result_failure_factory(self):
        """Test failure factory method"""
        result = PaymentResult.failure(
            request_id="REQ-123",
            message="Payment failed"
        )
        
        assert result.status == PaymentStatus.FAILED
        assert result.message == "Payment failed"
        assert result.transaction_id is None
        assert result.processed_at is not None
        assert result.is_successful is False
    
    def test_is_successful_property(self):
        """Test is_successful property"""
        success_result = PaymentResult(
            request_id="REQ-123",
            status=PaymentStatus.SUCCESS,
            message="Success"
        )
        
        failed_result = PaymentResult(
            request_id="REQ-124",
            status=PaymentStatus.FAILED,
            message="Failed"
        )
        
        assert success_result.is_successful is True
        assert failed_result.is_successful is False