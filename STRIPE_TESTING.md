# Stripe Payment Testing Guide

This guide will help you test the Stripe payment functionality in your Django e-commerce site.

## Prerequisites

1. **Stripe Account**: Create a free account at [stripe.com](https://stripe.com)
2. **API Keys**: Get your test API keys from the Stripe Dashboard
3. **Environment Setup**: Configure your `.env` file with Stripe credentials

## 1. Setting Up Stripe Test Keys

### Get Your Stripe Test Keys

1. Go to [Stripe Dashboard](https://dashboard.stripe.com/)
2. Make sure you're in **Test mode** (toggle in the left sidebar)
3. Go to **Developers → API Keys**
4. Copy your keys:
   - **Publishable key**: `pk_test_...`
   - **Secret key**: `sk_test_...`

### Configure Environment Variables

Create a `.env` file in your project root if it doesn't exist:

```bash
# Stripe Configuration
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
STRIPE_SECRET_KEY=sk_test_your_secret_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here
```

## 2. Test Card Numbers

### Successful Payments
- **Visa**: `4242424242424242`
- **Mastercard**: `5555555555554444`
- **American Express**: `378282246310005`

### Declined Payments
- **Generic decline**: `4000000000000002`
- **Insufficient funds**: `4000000000009995`
- **Lost card**: `4000000000009987`
- **Stolen card**: `4000000000009979`

### Special Scenarios
- **Requires authentication**: `4000002500003155`
- **Processing error**: `4000000000000119`
- **Incorrect CVC**: `4000000000000127`
- **Expired card**: `4000000000000069`

### Test Card Details
For all test cards, use:
- **Expiry**: Any future date (e.g., 12/25)
- **CVC**: Any 3-digit number (e.g., 123)
- **ZIP**: Any valid postal code (e.g., 12345)

## 3. Testing Workflow

### Step-by-Step Testing

1. **Start the Django Server**
   ```bash
   python manage.py runserver
   ```

2. **Add Products to Cart**
   - Go to `http://127.0.0.1:8000/`
   - Browse products and add items to cart

3. **Initiate Checkout**
   - Go to cart and click "Checkout"
   - Fill in order details
   - Select "Credit Card (Stripe)" as payment method

4. **Test Payment Scenarios**

   **Successful Payment:**
   - Use card: `4242424242424242`
   - Expiry: `12/25`
   - CVC: `123`
   - Complete payment and verify order confirmation

   **Declined Payment:**
   - Use card: `4000000000000002`
   - Verify error message appears
   - Test retry functionality

   **Authentication Required:**
   - Use card: `4000002500003155`
   - Complete 3D Secure authentication flow

## 4. Testing Commands and Scripts

### Test Stripe Service Directly

Create a test script to verify Stripe integration:

```python
# test_stripe.py
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_site.settings')
django.setup()

from orders.stripe_service import StripePaymentService, get_test_card_info

def test_stripe_service():
    service = StripePaymentService()
    
    # Test payment intent creation
    print("Testing Payment Intent Creation...")
    result = service.create_payment_intent(
        amount_cents=1000,  # $10.00
        currency='usd',
        customer_email='test@example.com'
    )
    
    if result['success']:
        print(f"✓ Payment Intent Created: {result['payment_intent']['id']}")
        print(f"✓ Client Secret: {result['client_secret'][:20]}...")
    else:
        print(f"✗ Error: {result['error']}")
    
    # Test card info
    print("\nAvailable Test Cards:")
    card_info = get_test_card_info()
    for category, cards in card_info.items():
        if isinstance(cards, dict):
            print(f"\n{category.replace('_', ' ').title()}:")
            for name, number in cards.items():
                print(f"  {name}: {number}")

if __name__ == "__main__":
    test_stripe_service()
```

Run the test:
```bash
python test_stripe.py
```

### Test Payment Processing

```python
# test_payment_flow.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_site.settings')
django.setup()

from orders.stripe_service import StripePaymentService

def test_full_payment_flow():
    service = StripePaymentService()
    
    # Create payment intent
    result = service.create_payment_intent(2500, customer_email='test@example.com')
    
    if result['success']:
        payment_intent_id = result['payment_intent']['id']
        print(f"Payment Intent: {payment_intent_id}")
        
        # Simulate payment confirmation check
        confirm_result = service.confirm_payment(payment_intent_id)
        print(f"Payment Status: {confirm_result.get('status', 'unknown')}")
    else:
        print(f"Failed to create payment: {result['error']}")

if __name__ == "__main__":
    test_full_payment_flow()
```

## 5. Testing Webhooks (Advanced)

### Using Stripe CLI

1. **Install Stripe CLI**
   ```bash
   # Download from https://github.com/stripe/stripe-cli/releases
   # Or use package manager
   ```

2. **Login to Stripe**
   ```bash
   stripe login
   ```

3. **Forward Webhooks to Local Server**
   ```bash
   stripe listen --forward-to localhost:8000/orders/stripe/webhook/
   ```

4. **Get Webhook Secret**
   The CLI will display a webhook secret like `whsec_...`
   Add this to your `.env` file as `STRIPE_WEBHOOK_SECRET`

5. **Test Webhook Events**
   ```bash
   stripe trigger payment_intent.succeeded
   ```

## 6. Common Issues and Solutions

### Issue: "No such payment_intent"
**Solution**: Make sure you're using the correct API keys and the payment intent was created successfully.

### Issue: "Invalid publishable key"
**Solution**: Verify your publishable key starts with `pk_test_` and is correctly set in settings.

### Issue: "Webhook signature verification failed"
**Solution**: Ensure the webhook secret matches the one from Stripe CLI or dashboard.

### Issue: CSRF token error on webhook
**Solution**: The webhook endpoint is decorated with `@csrf_exempt` - this is normal for webhooks.

## 7. Monitoring and Logs

### Check Django Logs
```bash
# In your Django terminal, you'll see payment processing logs
python manage.py runserver
```

### Check Stripe Dashboard
1. Go to [Stripe Dashboard](https://dashboard.stripe.com/)
2. Navigate to **Payments** to see test transactions
3. Check **Events** for webhook deliveries
4. Use **Logs** for debugging API calls

## 8. Production Checklist

When ready for production:

1. **Switch to Live Keys**
   - Replace `pk_test_` with `pk_live_`
   - Replace `sk_test_` with `sk_live_`

2. **Configure Real Webhooks**
   - Set up webhook endpoints in Stripe Dashboard
   - Use production webhook secrets

3. **Security Considerations**
   - Never expose secret keys in frontend code
   - Use environment variables for all credentials
   - Validate webhook signatures
   - Implement proper error handling

4. **Testing in Production**
   - Use small amounts for initial tests
   - Monitor all transactions carefully
   - Have a refund process ready

## 9. Troubleshooting Commands

### Test Stripe Configuration
```bash
python manage.py shell
```

```python
from django.conf import settings
print("Stripe Publishable Key:", settings.STRIPE_PUBLISHABLE_KEY[:20] + "...")
print("Stripe Secret Key:", "sk_test" in settings.STRIPE_SECRET_KEY)

# Test service import
from orders.stripe_service import StripePaymentService
service = StripePaymentService()
print("Stripe service loaded successfully")
```

### Check Database
```python
from orders.models import Order, Payment

# Check recent orders
orders = Order.objects.all().order_by('-created')[:5]
for order in orders:
    print(f"Order {order.id}: {order.payment_method} - ${order.get_total_cost()}")

# Check payments
payments = Payment.objects.all().order_by('-created_at')[:5]
for payment in payments:
    print(f"Payment {payment.id}: {payment.status} - {payment.payment_method}")
```

This comprehensive guide should help you test all aspects of the Stripe integration!