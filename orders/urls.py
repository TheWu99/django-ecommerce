from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('history/', views.order_history, name='order_history'),
    path('<int:order_id>/retry/', views.payment_retry, name='payment_retry'),
    
    # Stripe payment URLs
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('<int:order_id>/stripe/success/', views.stripe_payment_success, name='stripe_payment_success'),
    path('<int:order_id>/stripe/cancel/', views.stripe_payment_cancel, name='stripe_payment_cancel'),
]