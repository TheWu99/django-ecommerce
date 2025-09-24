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

## 🚀 Production Deployment

### Prerequisites
- Linux server (Ubuntu 20.04+ recommended)
- Python 3.8+
- PostgreSQL or MySQL database
- Nginx web server
- Domain name with SSL certificate

### Step 1: Server Setup

#### 1.1 Update System
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-dev python3-venv nginx postgresql postgresql-contrib
```

#### 1.2 Create Application User
```bash
sudo adduser django
sudo usermod -aG sudo django
su - django
```

#### 1.3 Setup PostgreSQL Database
```bash
sudo -u postgres psql

CREATE DATABASE django_ecommerce;
CREATE USER django_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE django_ecommerce TO django_user;
ALTER USER django_user CREATEDB;
\q
```

### Step 2: Application Deployment

#### 2.1 Clone Repository
```bash
cd /home/django
git clone https://github.com/YOUR_USERNAME/django-ecommerce-site.git
cd django-ecommerce-site
```

#### 2.2 Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

#### 2.3 Install Dependencies
```bash
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

#### 2.4 Environment Configuration
```bash
cp .env.example .env
nano .env
```

**Production .env file:**
```bash
# Django Settings
DEBUG=False
SECRET_KEY=your_super_secret_key_here_make_it_long_and_random
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database Configuration
DATABASE_URL=postgres://django_user:your_secure_password@localhost:5432/django_ecommerce

# Stripe Live Keys (replace with your live keys)
STRIPE_PUBLISHABLE_KEY=pk_live_your_live_publishable_key
STRIPE_SECRET_KEY=sk_live_your_live_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Email Configuration (for production)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

# Security Settings
SECURE_SSL_REDIRECT=True
SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

#### 2.5 Database Migration
```bash
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Step 3: Gunicorn Setup

#### 3.1 Test Gunicorn
```bash
gunicorn --bind 0.0.0.0:8000 ecommerce_site.wsgi:application
```

#### 3.2 Create Gunicorn Service
```bash
sudo nano /etc/systemd/system/django-ecommerce.service
```

**Service file content:**
```ini
[Unit]
Description=Django E-commerce Gunicorn daemon
After=network.target

[Service]
User=django
Group=www-data
WorkingDirectory=/home/django/django-ecommerce-site
ExecStart=/home/django/django-ecommerce-site/.venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/home/django/django-ecommerce-site/django-ecommerce.sock \
          ecommerce_site.wsgi:application

[Install]
WantedBy=multi-user.target
```

#### 3.3 Start and Enable Service
```bash
sudo systemctl start django-ecommerce
sudo systemctl enable django-ecommerce
sudo systemctl status django-ecommerce
```

### Step 4: Nginx Configuration

#### 4.1 Create Nginx Configuration
```bash
sudo nano /etc/nginx/sites-available/django-ecommerce
```

**Nginx configuration:**
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Certificate (use Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # SSL Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers off;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    
    location = /favicon.ico { 
        access_log off; 
        log_not_found off; 
    }
    
    # Static files
    location /static/ {
        root /home/django/django-ecommerce-site;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Media files
    location /media/ {
        root /home/django/django-ecommerce-site;
        expires 7d;
        add_header Cache-Control "public";
    }
    
    # Main application
    location / {
        include proxy_params;
        proxy_pass http://unix:/home/django/django-ecommerce-site/django-ecommerce.sock;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' https://js.stripe.com https://api.stripe.com; script-src 'self' 'unsafe-inline' https://js.stripe.com; style-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com; img-src 'self' data: https:; font-src 'self';" always;
}
```

#### 4.2 Enable Site and Restart Nginx
```bash
sudo ln -s /etc/nginx/sites-available/django-ecommerce /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 5: SSL Certificate (Let's Encrypt)

#### 5.1 Install Certbot
```bash
sudo apt install certbot python3-certbot-nginx
```

#### 5.2 Obtain SSL Certificate
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

#### 5.3 Auto-Renewal
```bash
sudo systemctl status certbot.timer
sudo certbot renew --dry-run
```

### Step 6: Stripe Webhook Configuration

#### 6.1 Configure Webhook Endpoint
1. Go to [Stripe Dashboard](https://dashboard.stripe.com/)
2. Navigate to **Developers → Webhooks**
3. Click **Add endpoint**
4. URL: `https://yourdomain.com/orders/stripe/webhook/`
5. Events: Select `payment_intent.succeeded` and `payment_intent.payment_failed`
6. Copy the webhook signing secret to your `.env` file

### Step 7: Monitoring and Maintenance

#### 7.1 Log Files
```bash
# Application logs
sudo journalctl -u django-ecommerce -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

#### 7.2 System Monitoring
```bash
# Check service status
sudo systemctl status django-ecommerce
sudo systemctl status nginx
sudo systemctl status postgresql

# Monitor resources
htop
df -h
```

#### 7.3 Database Backup
```bash
# Create backup script
nano /home/django/backup_db.sh
```

**Backup script:**
```bash
#!/bin/bash
DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/home/django/backups"
mkdir -p $BACKUP_DIR

pg_dump -U django_user -h localhost django_ecommerce > $BACKUP_DIR/django_ecommerce_$DATE.sql

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
```

```bash
chmod +x /home/django/backup_db.sh

# Add to crontab for daily backups
crontab -e
# Add: 0 2 * * * /home/django/backup_db.sh
```

### Step 8: Performance Optimization

#### 8.1 Install Redis (for caching)
```bash
sudo apt install redis-server
pip install django-redis
```

#### 8.2 Update Django Settings for Production
Add to `settings.py`:
```python
# Caching
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Session storage
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

### Step 9: Deployment Checklist

✅ **Security:**
- [ ] `DEBUG = False`
- [ ] Strong `SECRET_KEY`
- [ ] `ALLOWED_HOSTS` configured
- [ ] SSL certificate installed
- [ ] Security headers configured
- [ ] Database credentials secured

✅ **Performance:**
- [ ] Static files collected and served by Nginx
- [ ] Database optimized
- [ ] Caching configured
- [ ] Gzip compression enabled

✅ **Monitoring:**
- [ ] Log rotation configured
- [ ] Database backups scheduled
- [ ] Uptime monitoring setup
- [ ] Error tracking configured

✅ **Stripe:**
- [ ] Live API keys configured
- [ ] Webhook endpoints set up
- [ ] Payment flow tested
- [ ] SSL verified for webhooks

### Step 10: Deployment Updates

#### 10.1 Update Application
```bash
cd /home/django/django-ecommerce-site
git pull origin main
source .venv/bin/activate
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
sudo systemctl restart django-ecommerce
```

#### 10.2 Zero-Downtime Deployment (Advanced)
```bash
# Use Blue-Green deployment with multiple Gunicorn workers
# Or implement rolling updates with load balancer
```

This comprehensive deployment guide ensures your Django e-commerce site runs securely and efficiently in production!

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