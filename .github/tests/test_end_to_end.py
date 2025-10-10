"""End-to-end tests"""
import pytest
from decimal import Decimal

from domain import PaymentMode, Money, PaymentRequest, TransactionType
from infrastructure.factories import ConcretePaymentProcessorFactory
from application.services import PaymentService

class TestEndToEnd:
    """End-to-end test scenarios"""
    
    def test_complete_payment_system_workflow(self):
        """Test complete payment system workflow"""
        # Setup system
        factory = ConcretePaymentProcessorFactory()
        service = PaymentService(factory)
        
        # Test scenario: Multiple payments with different modes
        test_scenarios = [
            {
                "mode": PaymentMode.PAYPAL,
                "amount": Decimal('150.75'),
                "description": "PayPal payment"
            },
            {
                "mode": PaymentMode.GOOGLEPAY,
                "amount": Decimal('99.99'),
                "description": "Google Pay payment"
            },
            {
                "mode": PaymentMode.CREDITCARD,
                "amount": Decimal('250.00'),
                "description": "Credit Card payment"
            }
        ]
        
        results = []
        
        # Process all payments
        for scenario in test_scenarios:
            request = PaymentRequest(
                payment_mode=scenario["mode"],
                amount=Money(scenario["amount"]),
                transaction_type=TransactionType.PURCHASE,
                metadata={"description": scenario["description"]}
            )
            
            result = service.process_payment(request)
            results.append(result)
        
        # Verify all payments were successful
        assert len(results) == 3
        assert all(result.is_successful for result in results)
        
        # Verify transaction IDs are unique and properly formatted
        transaction_ids = [result.transaction_id for result in results]
        assert len(set(transaction_ids)) == 3
        
        # Verify correct prefixes
        assert results[0].transaction_id.startswith("PP_")  # PayPal
        assert results[1].transaction_id.startswith("GP_")  # Google Pay
        assert results[2].transaction_id.startswith("CC_")  # Credit Card
    
    def test_system_robustness_with_edge_cases(self):
        """Test system robustness with edge cases"""
        factory = ConcretePaymentProcessorFactory()
        service = PaymentService(factory)
        
        edge_cases = [
            # Minimum valid amount
            {
                "mode": PaymentMode.PAYPAL,
                "amount": Decimal('0.01'),
                "should_succeed": True
            },
            # Maximum valid amount
            {
                "mode": PaymentMode.CREDITCARD,
                "amount": Decimal('9999.99'),
                "should_succeed": True
            },
            # Zero amount (should fail)
            {
                "mode": PaymentMode.GOOGLEPAY,
                "amount": Decimal('0.00'),
                "should_succeed": False
            },
            # Amount exceeding limit (should fail)
            {
                "mode": PaymentMode.PAYPAL,
                "amount": Decimal('10001.00'),
                "should_succeed": False
            }
        ]
        
        for case in edge_cases:
            request = PaymentRequest(
                payment_mode=case["mode"],
                amount=Money(case["amount"]),
                transaction_type=TransactionType.PURCHASE
            )
            
            result = service.process_payment(request)
            
            if case["should_succeed"]:
                assert result.is_successful, f"Expected success for amount {case['amount']}"
            else:
                assert not result.is_successful, f"Expected failure for amount {case['amount']}"
    
    def test_system_extensibility(self):
        """Test that system can be extended with new processors"""
        factory = ConcretePaymentProcessorFactory()
        
        # Verify initial supported modes
        initial_modes = factory.get_supported_modes()
        assert len(initial_modes) == 3
        
        # Test that factory can be extended (conceptually)
        assert factory.is_supported(PaymentMode.PAYPAL)
        assert factory.is_supported(PaymentMode.GOOGLEPAY)
        assert factory.is_supported(PaymentMode.CREDITCARD)
    
    def test_concurrent_payment_processing(self):
        """Test concurrent payment processing"""
        import threading
        import time
        
        factory = ConcretePaymentProcessorFactory()
        service = PaymentService(factory)
        results = []
        
        def process_payment(payment_mode, amount):
            request = PaymentRequest(
                payment_mode=payment_mode,
                amount=Money(amount),
            )
            result = service.process_payment(request)
            results.append(result)
        
        # Create multiple threads
        threads = []
        test_data = [
            (PaymentMode.PAYPAL, Decimal('100.00')),
            (PaymentMode.GOOGLEPAY, Decimal('200.00')),
            (PaymentMode.CREDITCARD, Decimal('300.00')),
        ]
        
        for mode, amount in test_data:
            thread = threading.Thread(target=process_payment, args=(mode, amount))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify all payments were successful
        assert len(results) == 3
        assert all(result.is_successful for result in results)
        
        # Verify unique transaction IDs
        transaction_ids = [result.transaction_id for result in results]
        assert len(set(transaction_ids)) == 3