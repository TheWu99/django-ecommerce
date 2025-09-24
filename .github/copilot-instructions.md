## Framework: Django (Python)
## Architecture: Model-View-Template (MVT)
## Styling: Tailwind CSS (or provide your own preference)
## Database: Default SQLite for development.
## Goal: Build a functional e-commerce website with product listings, a shopping cart, and a checkout process.
# AI Coding Agent Instructions for This Codebase

## Project Overview
- **Framework:** Django 5.x (Python)
- **Architecture:** Model-View-Template (MVT)
- **Styling:** Tailwind CSS (planned, not yet present)
- **Database:** SQLite (default, see `settings.py`)
- **Goal:** E-commerce site with product listings, cart, and checkout (feature scaffolding only; business logic not yet implemented)

## Directory Structure & Key Files
- `ecommerce_site/`: Django project config (settings, URLs, WSGI/ASGI)
- `shop/`: Main app for e-commerce features (models, views, admin, tests)
- `manage.py`: Entrypoint for all Django CLI commands

## Developer Workflows
- **Run server:** `python manage.py runserver` (default port 8000)
- **Migrate DB:** `python manage.py makemigrations` then `python manage.py migrate`
- **Create superuser:** `python manage.py createsuperuser` (for admin site)
- **Run tests:** `python manage.py test shop`
- **Admin panel:** `/admin/` (enable models in `shop/admin.py`)

## Patterns & Conventions
- **Apps:** Each feature is a Django app (see `shop/`).
- **Models:** Define in `shop/models.py`, register in `shop/admin.py` for admin UI.
- **Views:** Use function-based views in `shop/views.py` (currently empty).
- **Templates:** Not present yet; add HTML files in `shop/templates/shop/` and configure `DIRS` in `settings.py` if needed.
- **Static files:** Use `STATIC_URL` in settings; Tailwind integration is planned but not set up.
- **Tests:** Use Django's `TestCase` in `shop/tests.py`.

## Integration Points
- **Django Admin:** Built-in, accessible at `/admin/` after running server and creating superuser.
- **Database:** SQLite file at `db.sqlite3` in project root.
- **External dependencies:** Only Django; add others to `requirements.txt` if needed.

## Project-Specific Notes
- No custom middleware, signals, or advanced patterns yet.
- No REST API, Celery, or third-party integrations present.
- All business logic, templates, and static assets are placeholders or missing; scaffold as needed.

## Example: Adding a Product Model
```python
# shop/models.py
class Product(models.Model):
	name = models.CharField(max_length=100)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	description = models.TextField(blank=True)
```
Register in `shop/admin.py`:
```python
from .models import Product
admin.site.register(Product)
```

## References
- [Django docs](https://docs.djangoproject.com/en/5.2/)
- Key files: `ecommerce_site/settings.py`, `shop/models.py`, `shop/views.py`, `shop/admin.py`

---
**Feedback:** If any section is unclear or missing, please specify which workflows, conventions, or integration points need more detail.