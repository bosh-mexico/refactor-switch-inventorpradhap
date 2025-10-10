"""Pytest configuration and fixtures"""
import pytest
from decimal import Decimal
from unittest.mock import Mock

from domain import PaymentMode, Money, PaymentRequest, TransactionType
from application.interfaces import PaymentProcessorFactory
from infrastructure.factories import ConcretePaymentProcessorFactory
from infrastructure.processors import PayPalProcessor, GooglePayProcessor, CreditCardProcessor
from application.services import PaymentService

@pytest.fixture
def sample_money():
    """Sample money fixture"""
    return Money(amount=Decimal('100.00'), currency='USD')

@pytest.fixture
def sample_payment_request(sample_money):
    """Sample payment request fixture"""
    return PaymentRequest(
        payment_mode=PaymentMode.PAYPAL,
        amount=sample_money,
        transaction_type=TransactionType.PURCHASE
    )

@pytest.fixture
def paypal_processor():
    """PayPal processor fixture"""
    return PayPalProcessor()

@pytest.fixture
def googlepay_processor():
    """Google Pay processor fixture"""
    return GooglePayProcessor()

@pytest.fixture
def creditcard_processor():
    """Credit Card processor fixture"""
    return CreditCardProcessor()

@pytest.fixture
def payment_factory():
    """Payment factory fixture"""
    return ConcretePaymentProcessorFactory()

@pytest.fixture
def mock_payment_factory():
    """Mock payment factory fixture"""
    factory = Mock(spec=PaymentProcessorFactory)
    factory.get_supported_modes.return_value = [
        PaymentMode.PAYPAL, 
        PaymentMode.GOOGLEPAY, 
        PaymentMode.CREDITCARD
    ]
    return factory

@pytest.fixture
def payment_service(payment_factory):
    """Payment service fixture"""
    return PaymentService(payment_factory)

@pytest.fixture
def mock_payment_service(mock_payment_factory):
    """Mock payment service fixture"""
    return PaymentService(mock_payment_factory)

@pytest.fixture
def valid_payment_amounts():
    """Valid payment amounts"""
    return [
        Decimal('0.01'),
        Decimal('100.00'),
        Decimal('999.99'),
        Decimal('9999.99')
    ]

@pytest.fixture
def invalid_payment_amounts():
    """Invalid payment amounts"""
    return [
        Decimal('0.00'),
        Decimal('-100.00'),
        Decimal('10001.00'),
        Decimal('99999.99')
    ]

@pytest.fixture
def all_payment_modes():
    """All payment modes"""
    return [PaymentMode.PAYPAL, PaymentMode.GOOGLEPAY, PaymentMode.CREDITCARD]