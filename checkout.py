from typing import Union
from payment_modes import PaymentMode
from payment_processor import PaymentProcessor

def checkout(mode: PaymentMode, amount: float) -> dict:
    """
    Main checkout function that processes payments based on the selected payment mode
    
    Args:
        mode (PaymentMode): The payment mode enum value
        amount (float): The payment amount
        
    Returns:
        dict: Payment processing result with status, transaction details, etc.
    """
    
    # Validate amount
    if amount <= 0:
        error_msg = f"Invalid amount: ${amount:.2f}. Amount must be greater than 0."
        print(f"Error: {error_msg}")
        return {
            "status": "error",
            "payment_mode": mode.name if hasattr(mode, 'name') else str(mode),
            "amount": amount,
            "transaction_id": None,
            "message": error_msg
        }
    
    print(f"\n--- Starting Checkout Process ---")
    print(f"Payment Mode: {mode.name if hasattr(mode, 'name') else 'Unknown'}")
    print(f"Amount: ${amount:.2f}")
    print("-" * 35)
    
    # Process payment based on mode
    try:
        if mode == PaymentMode.PAYPAL:
            result = PaymentProcessor.process_paypal_payment(amount)
        elif mode == PaymentMode.GOOGLEPAY:
            result = PaymentProcessor.process_googlepay_payment(amount)
        elif mode == PaymentMode.CREDITCARD:
            result = PaymentProcessor.process_creditcard_payment(amount)
        else:
            result = PaymentProcessor.handle_invalid_payment(mode, amount)
            
        print("-" * 35)
        print(f"Checkout Status: {result['status'].upper()}")
        print(f"--- End Checkout Process ---\n")
        
        return result
        
    except Exception as e:
        error_msg = f"Unexpected error during payment processing: {str(e)}"
        print(f"Error: {error_msg}")
        return {
            "status": "error",
            "payment_mode": mode.name if hasattr(mode, 'name') else str(mode),
            "amount": amount,
            "transaction_id": None,
            "message": error_msg
        }

def validate_payment_mode(mode_input: Union[str, int, PaymentMode]) -> PaymentMode:
    """
    Validate and convert input to PaymentMode enum
    
    Args:
        mode_input: Input that should represent a payment mode
        
    Returns:
        PaymentMode: Valid PaymentMode enum value or UNKNOWN
    """
    if isinstance(mode_input, PaymentMode):
        return mode_input
    
    if isinstance(mode_input, str):
        mode_map = {
            'paypal': PaymentMode.PAYPAL,
            'googlepay': PaymentMode.GOOGLEPAY,
            'googleplay': PaymentMode.GOOGLEPAY,  # Common typo
            'creditcard': PaymentMode.CREDITCARD,
            'credit_card': PaymentMode.CREDITCARD,
            'cc': PaymentMode.CREDITCARD
        }
        return mode_map.get(mode_input.lower(), PaymentMode.UNKNOWN)
    
    if isinstance(mode_input, int):
        try:
            return PaymentMode(mode_input)
        except ValueError:
            return PaymentMode.UNKNOWN
    
    return PaymentMode.UNKNOWN