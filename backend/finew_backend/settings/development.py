from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# CORS Configuration for development
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',  # Vite dev server
    'http://127.0.0.1:5173',
    'http://localhost:3000',
]

CORS_ALLOW_CREDENTIALS = True
