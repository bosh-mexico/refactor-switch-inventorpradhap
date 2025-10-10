"""Integration tests for payment flow"""
import pytest
from decimal import Decimal

from domain import PaymentMode, Money, PaymentRequest, TransactionType, PaymentStatus
from infrastructure.factories import ConcretePaymentProcessorFactory
from application.services import PaymentService

class TestIntegrationPaymentFlow:
    """Integration tests for complete payment flow"""
    
    @pytest.fixture
    def payment_service(self):
        """Payment service with real dependencies"""
        factory = ConcretePaymentProcessorFactory()
        return PaymentService(factory)
    
    @pytest.mark.parametrize("payment_mode", [
        PaymentMode.PAYPAL,
        PaymentMode.GOOGLEPAY,
        PaymentMode.CREDITCARD
    ])
    def test_complete_payment_flow_success(self, payment_service, payment_mode):
        """Test complete payment flow for all payment modes"""
        # Create request
        request = PaymentRequest(
            payment_mode=payment_mode,
            amount=Money(Decimal('100.00')),
            transaction_type=TransactionType.PURCHASE,
            metadata={"test": "integration"}
        )
        
        # Process payment
        result = payment_service.process_payment(request)
        
        # Verify result
        assert result.is_successful is True
        assert result.transaction_id is not None
        assert result.processed_at is not None
        assert payment_mode.value.replace('pay', ' Pay').title() in result.message or payment_mode.value.title() in result.message
    
    def test_payment_flow_with_invalid_amount(self, payment_service):
        """Test payment flow with invalid amount"""
        request = PaymentRequest(
            payment_mode=PaymentMode.PAYPAL,
            amount=Money(Decimal('0.00')),
        )
        
        result = payment_service.process_payment(request)
        
        assert result.is_successful is False
        assert "positive" in result.message.lower()
    
    def test_payment_flow_with_amount_too_high(self, payment_service):
        """Test payment flow with amount exceeding limit"""
        request = PaymentRequest(
            payment_mode=PaymentMode.CREDITCARD,
            amount=Money(Decimal('15000.00')),
        )
        
        result = payment_service.process_payment(request)
        
        assert result.is_successful is False
        assert "maximum limit" in result.message
    
    def test_get_supported_modes_integration(self, payment_service):
        """Test getting supported modes integration"""
        modes = payment_service.get_supported_payment_modes()
        
        expected_modes = [PaymentMode.PAYPAL, PaymentMode.GOOGLEPAY, PaymentMode.CREDITCARD]
        assert all(mode in modes for mode in expected_modes)
        assert len(modes) == len(expected_modes)
    
    def test_transaction_id_uniqueness(self, payment_service):
        """Test that transaction IDs are unique"""
        request = PaymentRequest(
            payment_mode=PaymentMode.PAYPAL,
            amount=Money(Decimal('100.00')),
        )
        
        # Process multiple payments
        results = [payment_service.process_payment(request) for _ in range(5)]
        
        # Verify all are successful
        assert all(result.is_successful for result in results)
        
        # Verify transaction IDs are unique
        transaction_ids = [result.transaction_id for result in results]
        assert len(set(transaction_ids)) == len(transaction_ids)

    @pytest.mark.parametrize("amount,expected_success", [
        (Decimal('0.01'), True),     # Minimum valid amount
        (Decimal('9999.99'), True),  # Maximum valid amount
        (Decimal('0.00'), False),    # Zero amount
        (Decimal('10001.00'), False) # Amount too high
    ])
    def test_amount_validation_integration(self, payment_service, amount, expected_success):
        """Test amount validation integration"""
        request = PaymentRequest(
            payment_mode=PaymentMode.PAYPAL,
            amount=Money(amount),
        )
        
        result = payment_service.process_payment(request)
        
        assert result.is_successful == expected_success