# LibraFlow
#### Libra Flow - Online Bookstore (E-Commerce API) built with Django, Django REST Framework, PostgreSQL, Celery, Redis, and Docker. A backend for an online bookstore with catalog management, shopping cart, and order processing. Implemented asynchronous tasks with Celery for order confirmation and email notifications.

# Quick Start
`
1. Clone the repository:`
   ```bash
   git clone
   ```
2. Navigate to the project directory:
   ```bash
   cd LibraFlow
   ```
3. Create a `.env` file in the root directory and add the following environment variables:
   ```env
    SECRET_KEY=your-secret-key-here
    DEBUG=your-debug-setting-here
    
    DB_NAME=your-database-name-here
    DB_USER=your-database-user-here
    DB_PASSWORD=your-database-password-here
    DB_PORT=your-database-port-here
    
    STRIPE_API_KEY=stripe-api-key-here
    STRIPE_WEBHOOK_SECRET=stripe-webhook-secret-here
   
    # Do not change the following lines
    DJANGO_SUPERUSER_USERNAME=admin
    DJANGO_SUPERUSER_EMAIL=admin@example.com
    DJANGO_SUPERUSER_PASSWORD=supersecret
4. Build and start the Docker containers:
   ```bash
   docker-compose up --build
   ```
   
# Admin User
#### Username: admin
#### Password: supersecret