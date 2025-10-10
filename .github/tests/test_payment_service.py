"""Tests for payment service"""
import pytest
from unittest.mock import Mock, patch
from decimal import Decimal

from domain import PaymentMode, Money, PaymentRequest, PaymentResult, PaymentStatus, InvalidPaymentModeError
from application.services import PaymentService
from application.interfaces import PaymentProcessorFactory, PaymentProcessor

class TestPaymentService:
    """Test payment service"""
    
    @pytest.fixture
    def mock_factory(self):
        """Mock factory fixture"""
        return Mock(spec=PaymentProcessorFactory)
    
    @pytest.fixture
    def mock_processor(self):
        """Mock processor fixture"""
        return Mock(spec=PaymentProcessor)
    
    @pytest.fixture
    def service(self, mock_factory):
        """Payment service fixture"""
        return PaymentService(mock_factory)
    
    @pytest.fixture
    def sample_request(self):
        """Sample payment request"""
        return PaymentRequest(
            payment_mode=PaymentMode.PAYPAL,
            amount=Money(Decimal('100.00'))
        )
    
    def test_process_payment_success(self, service, mock_factory, mock_processor, sample_request):
        """Test successful payment processing"""
        # Setup mocks
        mock_factory.create_processor.return_value = mock_processor
        mock_processor.process_payment.return_value = PaymentResult.success(
            request_id="REQ-123",
            transaction_id="TXN-456"
        )
        
        # Execute
        result = service.process_payment(sample_request)
        
        # Verify
        assert result.is_successful is True
        assert result.transaction_id == "TXN-456"
        mock_factory.create_processor.assert_called_once_with(PaymentMode.PAYPAL)
        mock_processor.process_payment.assert_called_once_with(sample_request)
    
    def test_process_payment_failure(self, service, mock_factory, mock_processor, sample_request):
        """Test failed payment processing"""
        # Setup mocks
        mock_factory.create_processor.return_value = mock_processor
        mock_processor.process_payment.return_value = PaymentResult.failure(
            request_id="REQ-123",
            message="Payment failed"
        )
        
        # Execute
        result = service.process_payment(sample_request)
        
        # Verify
        assert result.is_successful is False
        assert "Payment failed" in result.message
    
    def test_process_payment_invalid_mode(self, service, mock_factory, sample_request):
        """Test processing payment with invalid mode"""
        # Setup mock to raise exception
        mock_factory.create_processor.side_effect = InvalidPaymentModeError("paypal")
        
        # Execute
        result = service.process_payment(sample_request)
        
        # Verify
        assert result.is_successful is False
        assert "Invalid payment mode" in result.message
    
    def test_process_payment_unexpected_error(self, service, mock_factory, sample_request):
        """Test processing payment with unexpected error"""
        # Setup mock to raise unexpected exception
        mock_factory.create_processor.side_effect = Exception("Network error")
        
        # Execute
        result = service.process_payment(sample_request)
        
        # Verify
        assert result.is_successful is False
        assert "Internal payment processing error" in result.message
    
    def test_get_supported_payment_modes(self, service, mock_factory):
        """Test getting supported payment modes"""
        expected_modes = [PaymentMode.PAYPAL, PaymentMode.GOOGLEPAY]
        mock_factory.get_supported_modes.return_value = expected_modes
        
        # Execute
        modes = service.get_supported_payment_modes()
        
        # Verify
        assert modes == expected_modes
        mock_factory.get_supported_modes.assert_called_once()
    
    @patch('application.services.logger')
    def test_logging_success(self, mock_logger, service, mock_factory, mock_processor, sample_request):
        """Test logging on successful payment"""
        # Setup mocks
        mock_factory.create_processor.return_value = mock_processor
        mock_processor.process_payment.return_value = PaymentResult.success(
            request_id="REQ-123",
            transaction_id="TXN-456"
        )
        
        # Execute
        service.process_payment(sample_request)
        
        # Verify logging calls
        mock_logger.info.assert_called()
    
    @patch('application.services.logger')
    def test_logging_failure(self, mock_logger, service, mock_factory, mock_processor, sample_request):
        """Test logging on failed payment"""
        # Setup mocks
        mock_factory.create_processor.return_value = mock_processor
        mock_processor.process_payment.return_value = PaymentResult.failure(
            request_id="REQ-123",
            message="Payment failed"
        )
        
        # Execute
        service.process_payment(sample_request)
        
        # Verify logging calls
        mock_logger.warning.assert_called()