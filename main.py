from payment_modes import PaymentMode
from checkout import checkout, validate_payment_mode

def demo_payments():
    """
    Demonstrate the payment system with various scenarios
    """
    print("=== Payment System Demo ===\n")
    
    # Test data
    test_amount = 150.75
    
    # Test all valid payment modes
    print("Testing Valid Payment Modes:")
    print("=" * 50)
    
    valid_modes = [
        PaymentMode.PAYPAL,
        PaymentMode.GOOGLEPAY,
        PaymentMode.CREDITCARD
    ]
    
    results = []
    for mode in valid_modes:
        result = checkout(mode, test_amount)
        results.append(result)
    
    # Test invalid payment mode
    print("Testing Invalid Payment Mode:")
    print("=" * 50)
    invalid_result = checkout(PaymentMode.UNKNOWN, test_amount)
    results.append(invalid_result)
    
    # Test invalid amount
    print("Testing Invalid Amount:")
    print("=" * 50)
    invalid_amount_result = checkout(PaymentMode.PAYPAL, -50.00)
    results.append(invalid_amount_result)
    
    # Test string input validation
    print("Testing String Input Validation:")
    print("=" * 50)
    string_inputs = ['paypal', 'googlepay', 'creditcard', 'bitcoin']
    
    for string_input in string_inputs:
        validated_mode = validate_payment_mode(string_input)
        print(f"Input: '{string_input}' -> Validated as: {validated_mode.name}")
        result = checkout(validated_mode, 75.50)
        results.append(result)
    
    # Summary
    print("\n" + "=" * 60)
    print("PAYMENT PROCESSING SUMMARY")
    print("=" * 60)
    
    successful_payments = [r for r in results if r['status'] == 'success']
    failed_payments = [r for r in results if r['status'] == 'error']
    
    print(f"Total Payments Processed: {len(results)}")
    print(f"Successful Payments: {len(successful_payments)}")
    print(f"Failed Payments: {len(failed_payments)}")
    
    if successful_payments:
        total_amount = sum(p['amount'] for p in successful_payments)
        print(f"Total Amount Processed: ${total_amount:.2f}")
    
    print("\nSuccessful Transactions:")
    for payment in successful_payments:
        print(f"  - {payment['payment_mode']}: ${payment['amount']:.2f} (ID: {payment['transaction_id']})")
    
    print("\nFailed Transactions:")
    for payment in failed_payments:
        print(f"  - {payment['payment_mode']}: ${payment['amount']:.2f} - {payment['message']}")

def interactive_payment():
    """
    Interactive payment system for user input
    """
    print("\n" + "=" * 60)
    print("INTERACTIVE PAYMENT SYSTEM")
    print("=" * 60)
    
    while True:
        try:
            print("\nSupported Payment Modes:")
            for mode in PaymentMode.get_supported_modes():
                print(f"  {mode.value}. {mode.name}")
            
            print("  0. Exit")
            
            choice = input("\nSelect payment mode (number or name): ").strip()
            
            if choice == '0' or choice.lower() == 'exit':
                print("Thank you for using our payment system!")
                break
            
            # Validate payment mode
            if choice.isdigit():
                payment_mode = validate_payment_mode(int(choice))
            else:
                payment_mode = validate_payment_mode(choice)
            
            # Get amount
            amount_input = input("Enter payment amount: $").strip()
            try:
                amount = float(amount_input)
            except ValueError:
                print("Invalid amount format. Please enter a valid number.")
                continue
            
            # Process payment
            result = checkout(payment_mode, amount)
            
            if result['status'] == 'success':
                print(f"\n✅ Payment Successful!")
                print(f"Transaction ID: {result['transaction_id']}")
            else:
                print(f"\n❌ Payment Failed!")
                print(f"Error: {result['message']}")
                
        except KeyboardInterrupt:
            print("\n\nPayment process interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Run demonstration
    demo_payments()
    
    # Run interactive mode
    interactive_choice = input("\nWould you like to try the interactive payment system? (y/n): ").strip().lower()
    if interactive_choice in ['y', 'yes']:
        interactive_payment()