"""Main application entry point"""
from enums import PaymentMode
from services import PaymentService
from utils import setup_logger

# Setup logging
logger = setup_logger(__name__)

def main():
    """Main function to demonstrate payment system"""
    # Create payment service
    payment_service = PaymentService()
    
    # Test data
    test_cases = [
        (PaymentMode.PAYPAL, 150.75),
        (PaymentMode.GOOGLEPAY, 99.99),
        (PaymentMode.CREDITCARD, 250.00),
        (PaymentMode.PAYPAL, -50.00),  # Invalid amount
        (PaymentMode.CREDITCARD, 15000.00),  # Amount too high
    ]
    
    print("=== Payment Processing Demo ===\n")
    
    # Display supported payment modes
    supported_modes = payment_service.get_supported_payment_modes()
    print(f"Supported payment modes: {[mode.value for mode in supported_modes]}\n")
    
    # Process test cases
    for mode, amount in test_cases:
        print(f"Processing {mode.value} payment of ${amount:.2f}")
        result = payment_service.checkout(mode, amount)
        
        if result.success:
            print(f"✅ Success: {result.message}")
            if result.transaction_id:
                print(f"   Transaction ID: {result.transaction_id}")
        else:
            print(f"❌ Failed: {result.message}")
        print()
    
    # Test invalid payment mode handling
    print("Testing payment mode validation:")
    try:
        # Test with string instead of enum
        result = payment_service.checkout("invalid_mode", 100.0)  # type: ignore
        print(f"❌ Result: {result.message}")
    except Exception as e:
        print(f"❌ Exception caught: {str(e)}")

if __name__ == "__main__":
    main()