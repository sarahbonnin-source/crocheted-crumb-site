# CRM System Documentation

## Overview
This CRM (Customer Relationship Management) system has been integrated into The Crocheted Crumb website to manage customers, products, orders, and inquiries. The system uses Google Cloud SQL (PostgreSQL), Firestore, and includes Stripe payment stubs for future payment processing.

## Architecture

### Technology Stack
- **Backend**: Flask (Python 3.11)
- **Database**: Google Cloud SQL (PostgreSQL)
- **NoSQL**: Google Firestore
- **Payments**: Stripe (Stub Implementation)
- **Deployment**: Google Cloud Run
- **Container**: Docker

### Key Components

#### 1. Database Layer (`database.py`)
- Connection pooling for PostgreSQL
- Firestore client management
- Schema initialization
- Error handling and fallbacks

#### 2. Data Models (`models.py`)
- **Customer**: Manage customer information and profiles
- **Product**: Product catalog management
- **Order**: Order processing and tracking
- **OrderItem**: Individual items within orders
- **Inquiry**: Customer inquiries from contact form

#### 3. Stripe Integration (`stripe_stubs.py`)
- Payment intent creation (stub)
- Payment processing (stub)
- Refund handling (stub)
- Webhook processing (stub)
- **Note**: All Stripe functionality is currently stubbed for development. Replace with real Stripe API calls for production.

#### 4. Admin Authentication (`admin_auth.py`)
- Session-based admin login
- Protected admin routes
- Credential verification

#### 5. Main Application (`app.py`)
- Public routes (products, cart, checkout)
- Admin routes (dashboard, management interfaces)
- Integration with all components

## Setup Instructions

### Prerequisites
1. Google Cloud Project (danielsbonnin-com)
2. Cloud SQL PostgreSQL instance
3. Firestore database
4. Stripe account (for production)

### Environment Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Configure your `.env` file with actual values:
   ```
   # Database Configuration
   DB_HOST=/cloudsql/danielsbonnin-com:us-central1:your-instance-name
   DB_NAME=crocheted_crumb
   DB_USER=your-db-user
   DB_PASSWORD=your-secure-db-password
   DB_PORT=5432

   # Firestore Configuration
   GOOGLE_CLOUD_PROJECT=danielsbonnin-com
   FIRESTORE_COLLECTION_PREFIX=sarah_site_

   # Stripe Configuration (use test keys for development)
   STRIPE_PUBLIC_KEY=pk_test_your_key_here
   STRIPE_SECRET_KEY=sk_test_your_key_here
   STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

   # Admin Configuration
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=change_to_secure_password

   # Flask Configuration
   SECRET_KEY=generate_a_random_secret_key_here
   FLASK_ENV=production
   PORT=8080
   ```

### Database Setup

1. **Create Database**: Ensure the PostgreSQL database exists:
   ```sql
   CREATE DATABASE crocheted_crumb;
   ```

2. **Initialize Schema**: The schema is automatically initialized on first run, or you can manually run:
   ```python
   from database import init_db_pool, init_database_schema
   init_db_pool()
   init_database_schema()
   ```

3. **Load Sample Data**:
   ```bash
   python generate_sample_data.py
   ```

   This will create:
   - 10 sample customers
   - 15 sample products
   - 20 sample orders
   - 10 sample inquiries

### Local Development

#### Using Docker (Recommended)
```bash
# Build the container
docker build -t crocheted-crumb-site .

# Run the container
docker run -p 8080:8080 --env-file .env crocheted-crumb-site
```

#### Using Python Directly
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Access the application at `http://localhost:8080`

### Cloud Deployment

The application automatically deploys to Google Cloud Run when you push to the main branch.

#### Manual Deployment
```bash
# Build and deploy using Cloud Build
gcloud builds submit --config cloudbuild.yaml
```

## Feature Guide

### Public Features

#### Product Catalog (`/products`)
- Browse all products
- Filter by category (plushies, wearables, home_decor, custom)
- View product details
- Add to cart

#### Shopping Cart (`/cart`)
- View cart items
- See total price
- Proceed to checkout

#### Checkout (`/checkout`)
- Enter customer information
- Review order
- Submit order (stub payment processing)
- Receive order confirmation

#### Contact Form (`/contact`)
- Submit inquiries
- Automatically saved to database
- Logged to Firestore for analytics

### Admin Features

#### Admin Login (`/admin/login`)
- Secure login with username/password
- Session management
- **Default credentials**: See `.env` file

#### Dashboard (`/admin/dashboard`)
- Overview statistics:
  - Total customers
  - Total orders
  - Total revenue
  - New inquiries
- Recent orders list
- Recent inquiries list

#### Customer Management (`/admin/customers`)
- List all customers
- Search by name or email
- View customer details
- View customer order history

#### Product Management (`/admin/products`)
- List all products
- Filter by category
- View product details
- Check inventory levels

#### Order Management (`/admin/orders`)
- List all orders
- Filter by status
- View order details
- Update order status
- View customer information

#### Inquiry Management (`/admin/inquiries`)
- List all inquiries
- Filter by status (new, responded, closed)
- View inquiry details
- Mark as responded/closed

## Database Schema

### Customers Table
```sql
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(50),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Products Table
```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    category VARCHAR(50) NOT NULL,
    image_url VARCHAR(500),
    stock_quantity INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Orders Table
```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    total_amount DECIMAL(10, 2) NOT NULL,
    stripe_payment_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Order Items Table
```sql
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price_at_purchase DECIMAL(10, 2) NOT NULL
);
```

### Inquiries Table
```sql
CREATE TABLE inquiries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'new',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    responded_at TIMESTAMP
);
```

## API Reference

### Models API

#### Customer
```python
from models import Customer

# Create customer
customer_id = Customer.create(name, email, phone=None, address=None)

# Get customer
customer = Customer.get_by_id(customer_id)
customer = Customer.get_by_email(email)

# List customers
customers = Customer.get_all(limit=100, offset=0)

# Search customers
results = Customer.search(query, limit=50)

# Update customer
success = Customer.update(customer_id, name=None, email=None, phone=None, address=None)
```

#### Product
```python
from models import Product

# Create product
product_id = Product.create(name, description, price, category, image_url=None, stock_quantity=0)

# Get product
product = Product.get_by_id(product_id)

# List products
products = Product.get_all(category=None, limit=100, offset=0)

# Update product
success = Product.update(product_id, name=None, description=None, price=None, ...)
```

#### Order
```python
from models import Order

# Create order
order_id = Order.create(customer_id, total_amount, status='pending', stripe_payment_id=None)

# Get order
order = Order.get_by_id(order_id)

# List orders
orders = Order.get_all(status=None, limit=100, offset=0)

# Update order status
success = Order.update_status(order_id, new_status)

# Get customer orders
orders = Order.get_customer_orders(customer_id)
```

#### Inquiry
```python
from models import Inquiry

# Create inquiry
inquiry_id = Inquiry.create(name, email, message, status='new')

# Get inquiry
inquiry = Inquiry.get_by_id(inquiry_id)

# List inquiries
inquiries = Inquiry.get_all(status=None, limit=100, offset=0)

# Update inquiry status
success = Inquiry.update_status(inquiry_id, new_status)
```

### Stripe Stubs API

```python
from stripe_stubs import create_payment_intent_stub, process_payment_stub

# Create payment intent (stub)
payment_intent = create_payment_intent_stub(amount=25.50, customer_email='customer@example.com')

# Process payment (stub)
result = process_payment_stub(payment_intent['id'])
```

**Important**: All Stripe functions are stubs. They return mock data and don't process real payments.

## Security Considerations

### Current Implementation
- ✅ Session-based authentication for admin
- ✅ No credentials in source code (environment variables)
- ✅ SQL injection prevention (parameterized queries)
- ✅ Password input type for admin login
- ✅ CSRF protection via Flask sessions
- ✅ `.gitignore` for sensitive files

### Production Recommendations
1. **Use strong admin passwords** (change from default)
2. **Enable HTTPS** (already handled by Cloud Run)
3. **Implement rate limiting** for login attempts
4. **Add email verification** for new customers
5. **Implement real Stripe integration** for payments
6. **Add audit logging** for admin actions
7. **Regular security updates** for dependencies
8. **Backup database** regularly

## Troubleshooting

### Database Connection Issues
```python
# Check database configuration
from database import init_db_pool
success = init_db_pool()
if not success:
    print("Check DB_HOST, DB_USER, DB_PASSWORD in .env")
```

### Schema Not Initialized
```python
# Manually initialize schema
from database import init_database_schema
init_database_schema()
```

### Firestore Connection Issues
```python
# Check Firestore configuration
from database import get_firestore_client
client = get_firestore_client()
if not client:
    print("Check GOOGLE_CLOUD_PROJECT in .env")
```

### Sample Data Not Loading
```bash
# Ensure database is initialized first
python generate_sample_data.py
```

### Admin Login Not Working
- Check `ADMIN_USERNAME` and `ADMIN_PASSWORD` in `.env`
- Ensure `SECRET_KEY` is set for Flask sessions
- Clear browser cookies and try again

## Maintenance

### Adding New Products
1. Use admin interface: `/admin/products`
2. Or use Python:
   ```python
   from models import Product
   Product.create(
       name="New Product",
       description="Description",
       price=29.99,
       category="plushies",
       stock_quantity=10
   )
   ```

### Managing Orders
1. View orders in admin: `/admin/orders`
2. Update status as needed (pending → paid → processing → shipped → delivered)

### Responding to Inquiries
1. View inquiries: `/admin/inquiries`
2. Mark as "responded" after contacting customer
3. Mark as "closed" when resolved

## Future Enhancements

### Planned Features
- [ ] Email notifications (order confirmations, inquiry responses)
- [ ] Real Stripe payment processing
- [ ] Product image uploads
- [ ] Advanced analytics dashboard
- [ ] Customer portal for order tracking
- [ ] Inventory management with alerts
- [ ] Multi-user admin system with roles
- [ ] REST API for mobile app
- [ ] Export data (CSV, PDF)
- [ ] Automated backups

### Migration Path for Production Stripe
1. Replace stub functions in `stripe_stubs.py` with real Stripe API calls
2. Update environment variables with production Stripe keys
3. Implement webhook verification
4. Add error handling for payment failures
5. Test with Stripe test cards first
6. Enable production mode

## Support

For issues or questions:
- Check the troubleshooting section
- Review error logs: `docker logs <container_id>`
- Contact: snbonnin@gmail.com

## License
© 2024 The Crocheted Crumb. All rights reserved.
