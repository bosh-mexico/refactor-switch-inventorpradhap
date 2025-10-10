"""Tests for domain enums"""
import pytest
from domain import PaymentMode, PaymentStatus, TransactionType

class TestPaymentMode:
    """Test PaymentMode enum"""
    
    def test_payment_mode_values(self):
        """Test payment mode enum values"""
        assert PaymentMode.PAYPAL.value == "paypal"
        assert PaymentMode.GOOGLEPAY.value == "googlepay"
        assert PaymentMode.CREDITCARD.value == "creditcard"
    
    def test_payment_mode_count(self):
        """Test number of payment modes"""
        assert len(PaymentMode) == 3
    
    def test_payment_mode_membership(self):
        """Test payment mode membership"""
        assert PaymentMode.PAYPAL in PaymentMode
        assert "invalid_mode" not in [mode.value for mode in PaymentMode]

class TestPaymentStatus:
    """Test PaymentStatus enum"""
    
    def test_payment_status_values(self):
        """Test payment status enum values"""
        statuses = [status for status in PaymentStatus]
        assert PaymentStatus.PENDING in statuses
        assert PaymentStatus.PROCESSING in statuses
        assert PaymentStatus.SUCCESS in statuses
        assert PaymentStatus.FAILED in statuses
        assert PaymentStatus.CANCELLED in statuses

class TestTransactionType:
    """Test TransactionType enum"""
    
    def test_transaction_type_values(self):
        """Test transaction type enum values"""
        types = [t_type for t_type in TransactionType]
        assert TransactionType.PURCHASE in types
        assert TransactionType.REFUND in types
        assert TransactionType.AUTHORIZATION in types