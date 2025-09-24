# Django E-commerce Site with Stripe Integration

A full-featured e-commerce website built with Django 5.x, featuring product listings, shopping cart functionality, order management, and secure Stripe payment processing.

## 🚀 Features

- **Product Catalog**: Browse products with detailed information and images
- **Shopping Cart**: Add, remove, and update item quantities
- **User Authentication**: Register, login, and manage profiles
- **Order Management**: Complete order history and tracking
- **Stripe Payments**: Secure payment processing with multiple payment methods
- **Payment Retry**: Failed payment retry functionality
- **Admin Interface**: Django admin for inventory and order management
- **Responsive Design**: Mobile-friendly UI with Tailwind CSS
- **Test Mode**: Comprehensive testing setup with Stripe test cards

## 🛠 Technology Stack

- **Framework**: Django 5.2.6 (Python)
- **Architecture**: Model-View-Template (MVT)
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Database**: SQLite (development), PostgreSQL ready
- **Payments**: Stripe API integration
- **Authentication**: Django built-in auth system
- **Environment**: Python virtual environment with pip

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/django-ecommerce-site.git
   cd django-ecommerce-site
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   
   # On Windows:
   .venv\Scripts\activate
   
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your settings (especially Stripe keys)
   ```

5. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Visit the site**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 💳 Stripe Integration

### Test Mode Setup

1. **Get Stripe Test Keys**
   - Sign up at [stripe.com](https://stripe.com)
   - Get test keys from the Stripe Dashboard
   - Update your `.env` file:
     ```
     STRIPE_PUBLISHABLE_KEY=pk_test_...
     STRIPE_SECRET_KEY=sk_test_...
     ```

2. **Test Card Numbers**
   - **Success**: `4242 4242 4242 4242`
   - **Declined**: `4000 0000 0000 0002`
   - **Requires Auth**: `4000 0025 0000 3155`
   - Use any future expiry date and any 3-digit CVC

3. **Testing Workflow**
   - Add products to cart
   - Go to checkout
   - Select "Credit Card (Stripe)"
   - Enter test card details
   - Complete payment flow

For detailed testing instructions, see `STRIPE_TESTING.md`

## 🏗 Project Structure

```
django-ecommerce-site/
├── ecommerce_site/          # Django project configuration
├── shop/                    # Product catalog app
│   ├── models.py           # Product models
│   ├── views.py            # Product views
│   ├── admin.py            # Admin configuration
│   └── templates/shop/     # Product templates
├── cart/                    # Shopping cart functionality
│   ├── cart.py             # Cart session management
│   ├── views.py            # Cart views
│   └── templates/cart/     # Cart templates
├── orders/                  # Order management & payments
│   ├── models.py           # Order and Payment models
│   ├── views.py            # Order processing views
│   ├── stripe_service.py   # Stripe integration
│   ├── payment_forms.py    # Payment forms
│   └── templates/orders/   # Order templates
├── accounts/               # User authentication
│   ├── forms.py            # User forms
│   ├── views.py            # Auth views
│   └── templates/accounts/ # Auth templates
├── static/                 # Static files (CSS, JS)
├── templates/              # Base templates
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── STRIPE_TESTING.md      # Stripe testing guide
```

## 🎯 Key Features

### E-commerce Core
- **Product Management**: Full CRUD operations for products
- **Category System**: Organize products by categories
- **Image Handling**: Product image upload and display
- **Inventory Tracking**: Stock management system

### Shopping Experience
- **Session-based Cart**: Persistent shopping cart
- **Cart Management**: Add, remove, update quantities
- **Order Processing**: Complete checkout workflow
- **Order History**: User order tracking and history

### Payment Processing
- **Stripe Integration**: Secure credit card processing
- **Multiple Payment Methods**: Credit card, PayPal, bank transfer
- **Payment Retry**: Handle failed payments gracefully
- **Transaction Tracking**: Complete payment audit trail

### User Management
- **Registration/Login**: Django authentication system
- **User Profiles**: Customer information management
- **Order History**: Personal order tracking
- **Admin Interface**: Staff management tools

## 🧪 Testing

### Run Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test shop
python manage.py test orders
```

### Stripe Testing
```bash
# Run Stripe integration test
python test_stripe_basic.py
```

## 🚀 Deployment

### Environment Variables
Set these in production:
- `DEBUG=False`
- `SECRET_KEY=<strong-secret-key>`
- `ALLOWED_HOSTS=yourdomain.com`
- `STRIPE_PUBLISHABLE_KEY=pk_live_...`
- `STRIPE_SECRET_KEY=sk_live_...`

### Static Files
```bash
python manage.py collectstatic --noinput
```

### Database Migration
```bash
python manage.py migrate --noinput
```

## 📝 Available URLs

- `/` - Product listings home page
- `/admin/` - Django admin interface
- `/accounts/login/` - User login
- `/accounts/register/` - User registration
- `/accounts/profile/` - User profile
- `/cart/` - Shopping cart
- `/orders/create/` - Checkout page
- `/orders/history/` - Order history
- `/orders/<id>/` - Order detail
- `/orders/<id>/retry/` - Payment retry

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Documentation**: Check the inline code comments and docstrings
- **Issues**: Create an issue on GitHub for bugs or feature requests
- **Testing Guide**: See `STRIPE_TESTING.md` for payment testing
- **Django Docs**: https://docs.djangoproject.com/
- **Stripe Docs**: https://stripe.com/docs

## 🎉 Acknowledgments

- Django community for the excellent framework
- Stripe for secure payment processing
- Tailwind CSS for responsive design components