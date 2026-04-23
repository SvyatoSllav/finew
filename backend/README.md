# FineW Backend API

Django REST API backend for FineW budget tracking application.

## Tech Stack

- Django 4.2.7
- Django REST Framework 3.14.0
- PostgreSQL
- JWT Authentication (djangorestframework-simplejwt)
- Google OAuth support

## Setup

### 1. Create virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment variables

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

### 3. Create PostgreSQL database

```bash
createdb finew
```

Or using psql:

```sql
CREATE DATABASE finew;
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Create superuser (optional)

```bash
python manage.py createsuperuser
```

### 6. Run development server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## API Documentation

Once the server is running, visit:

- Swagger UI: `http://localhost:8000/api/schema/swagger-ui/`
- ReDoc: `http://localhost:8000/api/schema/redoc/`

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register with email/password
- `POST /api/auth/login/` - Login with email/password
- `POST /api/auth/google/` - Google OAuth login
- `POST /api/auth/token/refresh/` - Refresh access token
- `GET /api/auth/me/` - Get current user
- `PATCH /api/auth/me/` - Update current user

### Budgets
- `GET /api/budgets/` - List user's budgets
- `POST /api/budgets/` - Create budget
- `GET /api/budgets/{id}/` - Get budget details
- `PATCH /api/budgets/{id}/` - Update budget
- `DELETE /api/budgets/{id}/` - Delete budget
- `POST /api/budgets/join/` - Join budget via invite code

### Categories
- `GET /api/categories/?budget={id}` - List categories
- `POST /api/categories/` - Create category
- `GET /api/categories/{id}/` - Get category
- `PATCH /api/categories/{id}/` - Update category
- `DELETE /api/categories/{id}/` - Delete category

### Transactions
- `GET /api/transactions/?budget={id}` - List transactions
- `POST /api/transactions/` - Create transaction
- `GET /api/transactions/{id}/` - Get transaction
- `PATCH /api/transactions/{id}/` - Update transaction
- `DELETE /api/transactions/{id}/` - Delete transaction

## Project Structure

```
backend/
├── finew_backend/          # Django project
│   ├── settings/          # Split settings (base, dev, prod)
│   └── urls.py
├── apps/                   # Django apps
│   ├── users/             # User authentication
│   ├── budgets/           # Budget management
│   ├── categories/        # Categories
│   └── transactions/      # Transactions
├── manage.py
└── requirements.txt
```
