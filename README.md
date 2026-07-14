# Information Systems Portal Starter (Django)

A modular Django starter project for building an Information Systems Portal.

## Stack
- Python 3.12 (via local `.venv`)
- Django 4.2.x (LTS)
- django-bootstrap5
- jQuery 3.7.x
- DataTables 1.13.x (Bootstrap 5 integration)
- Chart.js 4.x
- SQLite (`db.sqlite3`)

## Frontend Libraries
- jQuery, DataTables, and Chart.js are loaded globally from CDN in `templates/base.html`.
- Child templates can initialize DataTables and charts inside the `extra_js` block.

## Project Layout
- `config/` - project settings, root URLs, ASGI/WSGI
- `apps/core/` - landing page and health endpoint
- `apps/accounts/` - login/logout URLs and auth templates
- `templates/` - shared and app templates
- `static/` - project-level static assets

## Quick Start
1. Create and activate a virtual environment.

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Run database migrations.

```bash
python manage.py migrate
```

4. (Optional) Create an admin user.

```bash
python manage.py createsuperuser
```

5. Start the development server.

```bash
python manage.py runserver
```

6. Open the app.
- Home: http://127.0.0.1:8000/
- Login: http://127.0.0.1:8000/accounts/login/
- Admin: http://127.0.0.1:8000/admin/
- Health: http://127.0.0.1:8000/health/

## Development Checks
Run framework validation:

```bash
python manage.py check
```

## Auth Behavior
- Login URL: `/accounts/login/`
- Logout URL: `/accounts/logout/`
- After login: redirects to home
- After logout: redirects to home

## Next Feature App
Use the existing modular pattern when adding features:
- Add new app under `apps/<feature>/`
- Mount routes in `config/urls.py`
- Keep templates in `templates/<feature>/`
