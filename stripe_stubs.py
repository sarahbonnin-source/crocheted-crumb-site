"""
Stripe payment integration stubs for development/testing.
This module provides stub implementations of Stripe payment functionality.
Replace with real Stripe API calls for production use.
"""
import os
import stripe
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

# Configure Stripe API key
stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_stub_key')

# Stripe public key for frontend
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', 'pk_test_stub_key')


def create_payment_intent_stub(amount: float, currency: str = 'usd', 
                                customer_email: str = None) -> Dict[str, Any]:
    """
    STUB: Create a Stripe payment intent.
    
    In production, this would call stripe.PaymentIntent.create()
    For now, it returns a mock successful response.
    
    Args:
        amount: Amount in dollars (will be converted to cents)
        currency: Currency code (default: 'usd')
        customer_email: Customer email for receipt
    
    Returns:
        Dict containing payment intent data
    """
    # Convert dollars to cents
    amount_cents = int(amount * 100)
    
    # STUB: Generate a fake payment intent ID
    fake_payment_intent_id = f"pi_stub_{int(amount_cents)}_{hash(customer_email or 'anonymous') % 100000}"
    
    # STUB: Return mock payment intent data
    stub_response = {
        'id': fake_payment_intent_id,
        'object': 'payment_intent',
        'amount': amount_cents,
        'currency': currency,
        'status': 'succeeded',  # STUB: Always succeed
        'client_secret': f"{fake_payment_intent_id}_secret_stub",
        'customer_email': customer_email,
        'metadata': {
            'stub': 'true',
            'note': 'This is a stub payment for development'
        }
    }
    
    print(f"✓ STUB: Created payment intent {fake_payment_intent_id} for ${amount}")
    return stub_response


def retrieve_payment_intent_stub(payment_intent_id: str) -> Optional[Dict[str, Any]]:
    """
    STUB: Retrieve a payment intent by ID.
    
    In production, this would call stripe.PaymentIntent.retrieve()
    For now, it returns a mock response.
    
    Args:
        payment_intent_id: The payment intent ID to retrieve
    
    Returns:
        Dict containing payment intent data or None if not found
    """
    # STUB: Return mock data for any ID
    if not payment_intent_id or not payment_intent_id.startswith('pi_'):
        return None
    
    stub_response = {
        'id': payment_intent_id,
        'object': 'payment_intent',
        'amount': 5000,  # $50.00 in cents
        'currency': 'usd',
        'status': 'succeeded',
        'metadata': {
            'stub': 'true'
        }
    }
    
    print(f"✓ STUB: Retrieved payment intent {payment_intent_id}")
    return stub_response


def process_payment_stub(payment_intent_id: str, payment_method: str = 'card_stub') -> Dict[str, Any]:
    """
    STUB: Process a payment.
    
    In production, this would confirm the payment intent and process the payment.
    For now, it returns a mock successful response.
    
    Args:
        payment_intent_id: The payment intent ID
        payment_method: Payment method ID (stub)
    
    Returns:
        Dict containing payment result
    """
    # STUB: Always return success
    result = {
        'success': True,
        'payment_intent_id': payment_intent_id,
        'status': 'succeeded',
        'message': 'STUB: Payment processed successfully',
        'amount_captured': 5000,  # cents
        'metadata': {
            'stub': 'true',
            'payment_method': payment_method
        }
    }
    
    print(f"✓ STUB: Processed payment {payment_intent_id}")
    return result


def create_refund_stub(payment_intent_id: str, amount: Optional[float] = None) -> Dict[str, Any]:
    """
    STUB: Create a refund for a payment.
    
    In production, this would call stripe.Refund.create()
    For now, it returns a mock successful response.
    
    Args:
        payment_intent_id: The payment intent ID to refund
        amount: Amount to refund in dollars (None for full refund)
    
    Returns:
        Dict containing refund data
    """
    refund_id = f"re_stub_{payment_intent_id}"
    
    stub_response = {
        'id': refund_id,
        'object': 'refund',
        'amount': int(amount * 100) if amount else None,
        'payment_intent': payment_intent_id,
        'status': 'succeeded',
        'metadata': {
            'stub': 'true'
        }
    }
    
    print(f"✓ STUB: Created refund {refund_id} for payment {payment_intent_id}")
    return stub_response


def handle_webhook_stub(payload: Dict[str, Any], signature: str = None) -> Dict[str, Any]:
    """
    STUB: Handle Stripe webhook events.
    
    In production, this would:
    1. Verify the webhook signature
    2. Parse the event
    3. Handle different event types
    
    For now, it returns a mock acknowledgment.
    
    Args:
        payload: Webhook payload
        signature: Webhook signature for verification
    
    Returns:
        Dict containing webhook handling result
    """
    event_type = payload.get('type', 'unknown')
    event_id = payload.get('id', 'evt_stub_unknown')
    
    # STUB: Acknowledge all webhook events
    result = {
        'received': True,
        'event_type': event_type,
        'event_id': event_id,
        'message': f'STUB: Webhook {event_type} acknowledged',
        'metadata': {
            'stub': 'true',
            'signature_verified': False  # STUB: Not verifying signatures
        }
    }
    
    print(f"✓ STUB: Handled webhook {event_type} ({event_id})")
    return result


def get_customer_payment_methods_stub(customer_email: str) -> list:
    """
    STUB: Get saved payment methods for a customer.
    
    In production, this would retrieve actual payment methods from Stripe.
    For now, it returns mock payment methods.
    
    Args:
        customer_email: Customer email
    
    Returns:
        List of payment method dicts
    """
    # STUB: Return mock payment methods
    stub_methods = [
        {
            'id': 'pm_stub_card_1',
            'type': 'card',
            'card': {
                'brand': 'visa',
                'last4': '4242',
                'exp_month': 12,
                'exp_year': 2025
            },
            'metadata': {'stub': 'true'}
        }
    ]
    
    print(f"✓ STUB: Retrieved {len(stub_methods)} payment methods for {customer_email}")
    return stub_methods


# Test function to verify Stripe configuration
def test_stripe_configuration():
    """Test function to verify Stripe stub configuration."""
    print("\n=== Testing Stripe Stub Configuration ===")
    
    # Test payment intent creation
    payment_intent = create_payment_intent_stub(
        amount=25.50,
        customer_email='test@example.com'
    )
    print(f"Payment Intent ID: {payment_intent['id']}")
    
    # Test payment processing
    result = process_payment_stub(payment_intent['id'])
    print(f"Payment Status: {result['status']}")
    
    # Test refund
    refund = create_refund_stub(payment_intent['id'], amount=10.00)
    print(f"Refund ID: {refund['id']}")
    
    # Test webhook handling
    webhook_payload = {
        'id': 'evt_test_webhook',
        'type': 'payment_intent.succeeded'
    }
    webhook_result = handle_webhook_stub(webhook_payload)
    print(f"Webhook Result: {webhook_result['message']}")
    
    print("\n✓ All Stripe stub tests passed!\n")


if __name__ == '__main__':
    test_stripe_configuration()
