# Django E-Commerce Project Setup Guide

## Prerequisites
- Python 3.8+ installed on your system
- Git (optional, for version control)

## Installation Instructions

### 1. Clone or Download the Project
```bash
# If using Git
git clone <repository-url>
cd django-ecommerce

# Or download and extract the project files
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# Or install minimal dependencies only
pip install -r requirements-minimal.txt
```

### 4. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configuration
# At minimum, set a SECRET_KEY
```

### 5. Database Setup
```bash
# Create database tables
python manage.py migrate

# Create superuser account
python manage.py createsuperuser

# Load sample data (optional)
python manage.py loaddata fixtures/sample_data.json
```

### 6. Static Files
```bash
# Collect static files (for production)
python manage.py collectstatic
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to see your e-commerce site!

## Project Features
- ✅ Product catalog with categories
- ✅ Shopping cart functionality
- ✅ User authentication (register/login)
- ✅ Order management system
- ✅ Payment processing (Credit Card, PayPal, Bank Transfer)
- ✅ Admin dashboard
- ✅ Responsive design with Tailwind CSS

## Available URLs
- `/` - Home page with product listings
- `/admin/` - Django admin interface
- `/accounts/login/` - User login
- `/accounts/register/` - User registration
- `/cart/` - Shopping cart
- `/orders/create/` - Checkout
- `/orders/history/` - Order history

## Development Commands

### Database Management
```bash
# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database (careful!)
python manage.py flush
```

### Testing
```bash
# Run tests
python manage.py test

# Or using pytest
pytest
```

### Package Management
```bash
# Add new package
pip install package-name
pip freeze > requirements.txt

# Update all packages
pip install --upgrade -r requirements.txt
```

## Production Deployment

### Environment Variables
Set these environment variables in production:
- `DEBUG=False`
- `SECRET_KEY=<strong-secret-key>`
- `ALLOWED_HOSTS=yourdomain.com`
- Database configuration
- Payment gateway keys

### Static Files
```bash
# Use WhiteNoise for static files (already configured)
python manage.py collectstatic --noinput
```

### Web Server
```bash
# Using Gunicorn (included in requirements)
gunicorn ecommerce_site.wsgi:application --bind 0.0.0.0:8000
```

## Troubleshooting

### Common Issues
1. **ModuleNotFoundError**: Make sure virtual environment is activated
2. **Database errors**: Run `python manage.py migrate`
3. **Static files not loading**: Run `python manage.py collectstatic`
4. **Permission errors on Windows**: Run PowerShell as Administrator

### Getting Help
- Check Django documentation: https://docs.djangoproject.com/
- Review project code comments
- Check error logs in terminal

## Optional Enhancements
Uncomment packages in requirements.txt for additional features:
- PostgreSQL/MySQL database support
- REST API with Django REST Framework
- Enhanced admin interface
- Caching with Redis
- Cloud storage with AWS S3
- Search functionality
- Social authentication