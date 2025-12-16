# Trading Platform

This is a Django-based trading platform that allows users to trade cryptocurrencies such as BTC, ETH, and others. The platform is built using the principles of Domain-Driven Design (DDD), which organizes the project into distinct domains, such as User Management, Trading, and others.

## Project Structure

The project follows DDD principles and is organized into domains and layers:

### `apps/`
The main business logic is organized into `apps/`. Each app corresponds to a different domain and its related functionality.

- **`user/`**: Manages user accounts, authentication, and permissions.
  - `application/`: Business logic and services related to user management.
  - `domain/`: Models and repositories for user data.
  - `presentation/`: API views and serializers for user-related requests.
  - `infrastructure/`: External services such as email handling.
  - `tests/`: Unit tests for user-related functionality.

- **`trading/`**: Handles trading functionality for cryptocurrencies.
  - `application/`: Logic related to placing orders, getting trading history, etc.
  - `domain/`: Models and repositories related to trades, orders, and charts.
  - `presentation/`: Views and serializers for trading-related requests.
  - `infrastructure/`: WebSocket connection for real-time trading updates.
  - `tests/`: Unit tests for trading-related functionality.

### `config/`
This folder contains all project-level settings and configurations.

- `settings/`: Project settings for different environments (development, production, testing).
- `urls/`: Global URL routing for all apps.
- `asgi.py` and `wsgi.py`: ASGI and WSGI entry points for running the project.

## Setup

### Requirements

- Python 3.x
- Django 4.x+
- Redis (for Celery)
- WebSocket for real-time updates

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/trading-platform.git
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up the database:
    ```bash
    python manage.py migrate
    ```

4. Create a superuser for accessing the Django Admin:
    ```bash
    python manage.py createsuperuser
    ```

5. Start the development server:
    ```bash
    python manage.py runserver
    ```

### Running Celery

Celery is used for background tasks like sending emails and processing long-running tasks.

1. Start Redis server:
    ```bash
    redis-server
    ```

2. Start Celery worker:
    ```bash
    celery -A config.celery worker --loglevel=info
    ```

3. Start Celery beat (for scheduled tasks):
    ```bash
    celery -A config.celery beat --loglevel=info
    ```

## Testing

To run tests, you can use Django's built-in test runner:
```bash
python manage.py test


$ python manage.py migrate --run-syncdb

& daphne -p 8000 Core.asgi:application