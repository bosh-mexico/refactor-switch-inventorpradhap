import unittest
from payment_modes import PaymentMode
from checkout import checkout, validate_payment_mode
from payment_processor import PaymentProcessor

class TestPaymentSystem(unittest.TestCase):
    """
    Unit tests for the payment system
    """
    
    def setUp(self):
        """Set up test data"""
        self.valid_amount = 100.50
        self.invalid_amount = -50.00
    
    def test_valid_payment_modes(self):
        """Test all valid payment modes"""
        valid_modes = [
            PaymentMode.PAYPAL,
            PaymentMode.GOOGLEPAY,
            PaymentMode.CREDITCARD
        ]
        
        for mode in valid_modes:
            result = checkout(mode, self.valid_amount)
            self.assertEqual(result['status'], 'success')
            self.assertEqual(result['amount'], self.valid_amount)
            self.assertIsNotNone(result['transaction_id'])
    
    def test_invalid_payment_mode(self):
        """Test invalid payment mode"""
        result = checkout(PaymentMode.UNKNOWN, self.valid_amount)
        self.assertEqual(result['status'], 'error')
        self.assertIsNone(result['transaction_id'])
    
    def test_invalid_amount(self):
        """Test invalid payment amount"""
        result = checkout(PaymentMode.PAYPAL, self.invalid_amount)
        self.assertEqual(result['status'], 'error')
        self.assertIn('Invalid amount', result['message'])
    
    def test_zero_amount(self):
        """Test zero amount"""
        result = checkout(PaymentMode.PAYPAL, 0.00)
        self.assertEqual(result['status'], 'error')
    
    def test_string_validation(self):
        """Test string input validation"""
        test_cases = {
            'paypal': PaymentMode.PAYPAL,
            'googlepay': PaymentMode.GOOGLEPAY,
            'creditcard': PaymentMode.CREDITCARD,
            'bitcoin': PaymentMode.UNKNOWN,
            'invalid': PaymentMode.UNKNOWN
        }
        
        for string_input, expected_mode in test_cases.items():
            validated_mode = validate_payment_mode(string_input)
            self.assertEqual(validated_mode, expected_mode)
    
    def test_integer_validation(self):
        """Test integer input validation"""
        test_cases = {
            1: PaymentMode.PAYPAL,
            2: PaymentMode.GOOGLEPAY,
            3: PaymentMode.CREDITCARD,
            99: PaymentMode.UNKNOWN,
            999: PaymentMode.UNKNOWN
        }
        
        for int_input, expected_mode in test_cases.items():
            validated_mode = validate_payment_mode(int_input)
            self.assertEqual(validated_mode, expected_mode)
    
    def test_payment_mode_validation(self):
        """Test PaymentMode enum validation"""
        mode = validate_payment_mode(PaymentMode.PAYPAL)
        self.assertEqual(mode, PaymentMode.PAYPAL)
    
    def test_is_valid_method(self):
        """Test PaymentMode.is_valid() method"""
        self.assertTrue(PaymentMode.is_valid(PaymentMode.PAYPAL))
        self.assertTrue(PaymentMode.is_valid(PaymentMode.GOOGLEPAY))
        self.assertTrue(PaymentMode.is_valid(PaymentMode.CREDITCARD))
        self.assertFalse(PaymentMode.is_valid(PaymentMode.UNKNOWN))

if __name__ == '__main__':
    unittest.main()