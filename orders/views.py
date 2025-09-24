from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import stripe
from cart.cart import Cart
from .models import Order, OrderItem, Payment
from .forms import OrderCreateForm
from .payment_forms import PaymentForm
from .stripe_service import StripePaymentService


def order_create(request):
    """
    Create a new order from the cart contents.
    """
    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart:cart_detail')
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST, user=request.user)
        payment_form = PaymentForm(request.POST)
        
        if form.is_valid() and payment_form.is_valid():
            # Create the order
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.payment_method = payment_form.cleaned_data['payment_method']
            order.save()
            
            # Create order items from cart
            total_cost = 0
            for item in cart:
                order_item = OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
                total_cost += order_item.get_cost()
            
            # Handle Stripe payments differently
            if payment_form.cleaned_data['payment_method'] == 'stripe':
                return _handle_stripe_payment(request, order, payment_form)
            else:
                # Create payment record for non-Stripe methods
                payment = Payment.objects.create(
                    order=order,
                    payment_method=payment_form.cleaned_data['payment_method'],
                    amount=total_cost,
                    payment_details=_get_payment_details(payment_form.cleaned_data)
                )
                
                # Process payment based on method
                payment_success = _process_payment(payment, payment_form.cleaned_data)
                
                if payment_success:
                    payment.mark_as_completed()
                    cart.clear()
                    messages.success(request, f'Order {order.id} has been created and payment processed successfully!')
                    return redirect('orders:order_detail', order_id=order.id)
                else:
                    payment.status = 'failed'
                    payment.save()
                    messages.error(request, 'Payment processing failed. Please try again.')
                    return redirect('orders:payment_retry', order_id=order.id)
    else:
        form = OrderCreateForm(user=request.user)
        payment_form = PaymentForm()
    
    # Add Stripe publishable key for frontend
    stripe_publishable_key = settings.STRIPE_PUBLISHABLE_KEY
    
    return render(request, 'orders/order/create.html', {
        'cart': cart,
        'form': form,
        'payment_form': payment_form,
        'stripe_publishable_key': stripe_publishable_key
    })


def _get_payment_details(payment_data):
    """Extract relevant payment details for storage"""
    details = {}
    
    if payment_data['payment_method'] == 'credit_card':
        details = {
            'cardholder_name': payment_data.get('cardholder_name'),
            'last_four_digits': payment_data.get('card_number', '')[-4:] if payment_data.get('card_number') else '',
            'expiry_month': payment_data.get('expiry_month'),
            'expiry_year': payment_data.get('expiry_year'),
        }
    elif payment_data['payment_method'] == 'paypal':
        details = {
            'paypal_email': payment_data.get('paypal_email'),
        }
    elif payment_data['payment_method'] == 'bank_transfer':
        details = {
            'bank_name': payment_data.get('bank_name'),
            'account_last_digits': payment_data.get('bank_account', '')[-4:] if payment_data.get('bank_account') else '',
        }
    
    return details


def _handle_stripe_payment(request, order, payment_form):
    """Handle Stripe payment processing"""
    stripe_service = StripePaymentService()
    
    # Get payment amount in cents
    amount_cents = stripe_service.dollars_to_cents(order.get_total_cost())
    
    # Create Payment Intent
    result = stripe_service.create_payment_intent(
        amount_cents=amount_cents,
        customer_email=order.email
    )
    
    if result['success']:
        # Create payment record
        payment = Payment.objects.create(
            order=order,
            payment_method='stripe',
            amount=order.get_total_cost(),
            transaction_id=result['payment_intent']['id'],
            status='pending'
        )
        
        # Redirect to Stripe payment page
        return render(request, 'orders/order/stripe_payment.html', {
            'order': order,
            'client_secret': result['client_secret'],
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
            'payment': payment
        })
    else:
        messages.error(request, f'Payment initialization failed: {result["error"]}')
        return redirect('orders:payment_retry', order_id=order.id)


def _process_payment(payment, payment_data):
    """
    Process payment based on the selected method.
    In a real application, this would integrate with payment gateways.
    """
    import random
    import time
    
    # Simulate payment processing
    time.sleep(1)  # Simulate network delay
    
    # For demo purposes, randomly succeed/fail payments
    # In production, integrate with Stripe, PayPal, etc.
    
    if payment_data['payment_method'] == 'stripe':
        # Stripe payments are handled separately via _handle_stripe_payment
        return True
    
    elif payment_data['payment_method'] == 'credit_card':
        # Simulate credit card processing
        success_rate = 0.9  # 90% success rate for demo
        if random.random() < success_rate:
            payment.transaction_id = f"CC_{random.randint(100000, 999999)}"
            return True
    
    elif payment_data['payment_method'] == 'paypal':
        # Simulate PayPal processing
        success_rate = 0.95  # 95% success rate for demo
        if random.random() < success_rate:
            payment.transaction_id = f"PP_{random.randint(100000, 999999)}"
            return True
    
    elif payment_data['payment_method'] == 'bank_transfer':
        # Bank transfers are usually manual verification
        payment.status = 'processing'  # Requires manual verification
        payment.transaction_id = f"BT_{random.randint(100000, 999999)}"
        payment.save()
        return True
    
    return False


def order_detail(request, order_id):
    """
    Display order details.
    """
    order = get_object_or_404(Order, id=order_id)
    
    # Only allow order owner or staff to view the order
    if request.user.is_authenticated:
        if order.user != request.user and not request.user.is_staff:
            messages.error(request, 'You do not have permission to view this order.')
            return redirect('shop:product_list')
    else:
        # For anonymous users, we could implement a session-based check
        # For now, redirect to login
        messages.error(request, 'Please log in to view your order.')
        return redirect('accounts:login')
    
    return render(request, 'orders/order/detail.html', {'order': order})


@login_required
def order_history(request):
    """
    Display order history for the logged-in user.
    """
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order/history.html', {'orders': orders})


def payment_retry(request, order_id):
    """
    Allow users to retry payment for a failed order.
    """
    order = get_object_or_404(Order, id=order_id)
    
    # Check permissions
    if request.user.is_authenticated:
        if order.user != request.user and not request.user.is_staff:
            messages.error(request, 'You do not have permission to access this order.')
            return redirect('shop:product_list')
    else:
        messages.error(request, 'Please log in to retry payment.')
        return redirect('accounts:login')
    
    # Check if order is already paid
    if order.paid:
        messages.info(request, 'This order has already been paid.')
        return redirect('orders:order_detail', order_id=order.id)
    
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            # Update or create payment record
            payment, created = Payment.objects.get_or_create(
                order=order,
                defaults={
                    'payment_method': payment_form.cleaned_data['payment_method'],
                    'amount': order.get_total_cost(),
                    'payment_details': _get_payment_details(payment_form.cleaned_data)
                }
            )
            
            if not created:
                # Update existing payment
                payment.payment_method = payment_form.cleaned_data['payment_method']
                payment.payment_details = _get_payment_details(payment_form.cleaned_data)
                payment.status = 'pending'
                payment.save()
            
            # Process payment
            payment_success = _process_payment(payment, payment_form.cleaned_data)
            
            if payment_success:
                payment.mark_as_completed()
                messages.success(request, 'Payment processed successfully!')
                return redirect('orders:order_detail', order_id=order.id)
            else:
                payment.status = 'failed'
                payment.save()
                messages.error(request, 'Payment processing failed. Please try again.')
    else:
        payment_form = PaymentForm()
    
    return render(request, 'orders/order/payment_retry.html', {
        'order': order,
        'payment_form': payment_form
    })


@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe webhooks for payment confirmation"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        
        # Find the payment by transaction_id
        try:
            payment = Payment.objects.get(transaction_id=payment_intent['id'])
            payment.mark_as_completed()
            
            # Clear any stored cart for this user (if session available)
            # Note: In webhook, we don't have access to user session
            
        except Payment.DoesNotExist:
            pass  # Payment not found, might be from another source
    
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        
        try:
            payment = Payment.objects.get(transaction_id=payment_intent['id'])
            payment.status = 'failed'
            payment.save()
        except Payment.DoesNotExist:
            pass

    return JsonResponse({'status': 'success'})


def stripe_payment_success(request, order_id):
    """Handle successful Stripe payment confirmation"""
    order = get_object_or_404(Order, id=order_id)
    
    # Verify payment status with Stripe
    try:
        payment = Payment.objects.get(order=order, payment_method='stripe')
        stripe_service = StripePaymentService()
        
        result = stripe_service.confirm_payment(payment.transaction_id)
        
        if result['success'] and result['status'] == 'succeeded':
            payment.mark_as_completed()
            
            # Clear cart
            cart = Cart(request)
            cart.clear()
            
            messages.success(request, f'Payment successful! Order #{order.id} has been confirmed.')
            return redirect('orders:order_detail', order_id=order.id)
        else:
            messages.error(request, 'Payment verification failed. Please contact support.')
            return redirect('orders:payment_retry', order_id=order.id)
            
    except Payment.DoesNotExist:
        messages.error(request, 'Payment record not found.')
        return redirect('orders:payment_retry', order_id=order.id)


def stripe_payment_cancel(request, order_id):
    """Handle cancelled Stripe payment"""
    order = get_object_or_404(Order, id=order_id)
    
    messages.warning(request, 'Payment was cancelled. You can try again.')
    return redirect('orders:payment_retry', order_id=order.id)
