from typing import Union
from payment_modes import PaymentMode

class PaymentProcessor:
    """
    Payment processor class to handle different payment modes
    """
    
    @staticmethod
    def process_paypal_payment(amount: float) -> dict:
        """
        Process PayPal payment
        """
        print(f"Processing PayPal payment of ${amount:.2f}")
        print("Connecting to PayPal API...")
        print("Payment processed successfully via PayPal")
        
        return {
            "status": "success",
            "payment_mode": "PayPal",
            "amount": amount,
            "transaction_id": f"PP_{hash(str(amount))}",
            "message": "PayPal payment completed successfully"
        }
    
    @staticmethod
    def process_googlepay_payment(amount: float) -> dict:
        """
        Process GooglePay payment
        """
        print(f"Processing GooglePay payment of ${amount:.2f}")
        print("Connecting to GooglePay API...")
        print("Payment processed successfully via GooglePay")
        
        return {
            "status": "success",
            "payment_mode": "GooglePay",
            "amount": amount,
            "transaction_id": f"GP_{hash(str(amount))}",
            "message": "GooglePay payment completed successfully"
        }
    
    @staticmethod
    def process_creditcard_payment(amount: float) -> dict:
        """
        Process Credit Card payment
        """
        print(f"Processing Credit Card payment of ${amount:.2f}")
        print("Connecting to Credit Card processing gateway...")
        print("Payment processed successfully via Credit Card")
        
        return {
            "status": "success",
            "payment_mode": "Credit Card",
            "amount": amount,
            "transaction_id": f"CC_{hash(str(amount))}",
            "message": "Credit Card payment completed successfully"
        }
    
    @staticmethod
    def handle_invalid_payment(mode: PaymentMode, amount: float) -> dict:
        """
        Handle invalid or unsupported payment modes
        """
        error_msg = f"Invalid or unsupported payment mode: {mode.name if hasattr(mode, 'name') else mode}"
        print(f"Error: {error_msg}")
        print(f"Supported payment modes: {[mode.name for mode in PaymentMode.get_supported_modes()]}")
        
        return {
            "status": "error",
            "payment_mode": mode.name if hasattr(mode, 'name') else str(mode),
            "amount": amount,
            "transaction_id": None,
            "message": error_msg
        }