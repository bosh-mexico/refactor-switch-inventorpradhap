"""Tests for payment factory"""
import pytest
from unittest.mock import Mock

from domain import PaymentMode, InvalidPaymentModeError
from infrastructure.factories import ConcretePaymentProcessorFactory
from infrastructure.processors import PayPalProcessor, GooglePayProcessor, CreditCardProcessor
from application.interfaces import PaymentProcessor

class TestConcretePaymentProcessorFactory:
    """Test payment processor factory"""
    
    def test_create_paypal_processor(self, payment_factory):
        """Test creating PayPal processor"""
        processor = payment_factory.create_processor(PaymentMode.PAYPAL)
        
        assert isinstance(processor, PayPalProcessor)
        assert processor.supports_payment_mode(PaymentMode.PAYPAL)
    
    def test_create_googlepay_processor(self, payment_factory):
        """Test creating Google Pay processor"""
        processor = payment_factory.create_processor(PaymentMode.GOOGLEPAY)
        
        assert isinstance(processor, GooglePayProcessor)
        assert processor.supports_payment_mode(PaymentMode.GOOGLEPAY)
    
    def test_create_creditcard_processor(self, payment_factory):
        """Test creating Credit Card processor"""
        processor = payment_factory.create_processor(PaymentMode.CREDITCARD)
        
        assert isinstance(processor, CreditCardProcessor)
        assert processor.supports_payment_mode(PaymentMode.CREDITCARD)
    
    def test_create_processor_invalid_mode(self, payment_factory):
        """Test creating processor with invalid mode"""
        # Clear processors to simulate unsupported mode
        payment_factory._processors = {}
        
        with pytest.raises(InvalidPaymentModeError):
            payment_factory.create_processor(PaymentMode.PAYPAL)
    
    def test_get_supported_modes(self, payment_factory):
        """Test getting supported modes"""
        modes = payment_factory.get_supported_modes()
        
        expected_modes = [PaymentMode.PAYPAL, PaymentMode.GOOGLEPAY, PaymentMode.CREDITCARD]
        assert all(mode in modes for mode in expected_modes)
        assert len(modes) == 3
    
    def test_register_processor(self, payment_factory):
        """Test registering new processor"""
        mock_processor_class = Mock(spec=PaymentProcessor)
        
        # Register new processor
        payment_factory.register_processor(PaymentMode.PAYPAL, mock_processor_class)
        
        # Verify the processor was registered
        assert payment_factory._processors[PaymentMode.PAYPAL] == mock_processor_class
    
    def test_is_supported(self, payment_factory):
        """Test checking if mode is supported"""
        assert payment_factory.is_supported(PaymentMode.PAYPAL) is True
        assert payment_factory.is_supported(PaymentMode.GOOGLEPAY) is True
        assert payment_factory.is_supported(PaymentMode.CREDITCARD) is True
        
        # Test with empty processors dict
        payment_factory._processors = {}
        assert payment_factory.is_supported(PaymentMode.PAYPAL) is False