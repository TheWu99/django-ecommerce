"""
Stripe Payment Service
Handles Stripe payment processing for the e-commerce site
"""
import stripe
from django.conf import settings
from decimal import Decimal

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class StripePaymentService:
    """Service class for handling Stripe payments"""
    
    def __init__(self):
        self.stripe = stripe
    
    def create_payment_intent(self, amount_cents, currency='usd', customer_email=None):
        """
        Create a Stripe Payment Intent
        
        Args:
            amount_cents (int): Amount in cents (e.g., $10.00 = 1000)
            currency (str): Currency code (default: 'usd')
            customer_email (str): Customer email for receipt
            
        Returns:
            dict: Payment Intent object or error
        """
        try:
            intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency=currency,
                metadata={
                    'customer_email': customer_email or 'test@example.com'
                },
                automatic_payment_methods={
                    'enabled': True,
                },
            )
            return {
                'success': True,
                'payment_intent': intent,
                'client_secret': intent.client_secret
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def confirm_payment(self, payment_intent_id):
        """
        Confirm a payment intent
        
        Args:
            payment_intent_id (str): Stripe Payment Intent ID
            
        Returns:
            dict: Confirmation result
        """
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            return {
                'success': True,
                'status': intent.status,
                'payment_intent': intent
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_test_token(self, card_number='4242424242424242'):
        """
        Create a test token for testing (use Stripe test cards)
        
        Args:
            card_number (str): Test card number
            
        Returns:
            dict: Token creation result
        """
        try:
            token = stripe.Token.create(
                card={
                    'number': card_number,
                    'exp_month': 12,
                    'exp_year': 2025,
                    'cvc': '123',
                }
            )
            return {
                'success': True,
                'token': token
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def dollars_to_cents(amount_dollars):
        """Convert dollar amount to cents"""
        return int(Decimal(str(amount_dollars)) * 100)
    
    @staticmethod
    def cents_to_dollars(amount_cents):
        """Convert cents to dollar amount"""
        return Decimal(amount_cents) / 100


# Test card numbers for different scenarios
TEST_CARDS = {
    'visa_success': '4242424242424242',
    'visa_declined': '4000000000000002',
    'mastercard_success': '5555555555554444',
    'amex_success': '378282246310005',
    'require_authentication': '4000002500003155',
    'insufficient_funds': '4000000000009995',
}


def get_test_card_info():
    """Return test card information for development"""
    return {
        'success_cards': {
            'Visa': '4242424242424242',
            'Mastercard': '5555555555554444',
            'American Express': '378282246310005',
        },
        'test_scenarios': {
            'Declined Payment': '4000000000000002',
            'Insufficient Funds': '4000000000009995',
            'Expired Card': '4000000000000069',
            '3D Secure Required': '4000002500003155',
        },
        'test_details': {
            'exp_month': 12,
            'exp_year': 2025,
            'cvc': '123',
            'zip': '12345'
        }
    }