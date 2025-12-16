# CRM System Requirements & Acceptance Criteria

## Project Overview
Implement a Customer Relationship Management (CRM) system for Sarah's Crocheted Crumb website with integration to Google Cloud SQL (PostgreSQL), Firestore, and Stripe payment processing stubs.

## Acceptance Criteria

### 1. Database Integration
**Cloud SQL (PostgreSQL)**
- [ ] Successfully connect to Cloud SQL instance on danielsbonnin.com project
- [ ] Create tables for: customers, products, orders, order_items, inquiries
- [ ] Support connection pooling for efficiency
- [ ] Handle connection errors gracefully with fallback
- [ ] Use environment variables for credentials (no hardcoded secrets)

**Firestore**
- [ ] Successfully connect to Firestore on danielsbonnin.com project
- [ ] Store: activity logs, analytics, session data
- [ ] Implement read/write operations
- [ ] Handle Firestore connection errors gracefully

### 2. CRM Data Models
**Customer Model**
- [ ] Fields: id, name, email, phone, address, created_at, updated_at
- [ ] Email validation
- [ ] Unique email constraint
- [ ] CRUD operations functional

**Product Model**
- [ ] Fields: id, name, description, price, category, image_url, stock_quantity, created_at
- [ ] Price validation (positive numbers)
- [ ] Categories: plushies, wearables, home_decor, custom
- [ ] CRUD operations functional

**Order Model**
- [ ] Fields: id, customer_id, status, total_amount, stripe_payment_id, created_at, updated_at
- [ ] Status values: pending, paid, processing, shipped, delivered, cancelled
- [ ] Foreign key to customer
- [ ] CRUD operations functional

**Order Items Model**
- [ ] Fields: id, order_id, product_id, quantity, price_at_purchase
- [ ] Foreign keys to order and product
- [ ] CRUD operations functional

**Inquiry Model**
- [ ] Fields: id, name, email, message, status, created_at, responded_at
- [ ] Status values: new, responded, closed
- [ ] CRUD operations functional

### 3. Sample Data
- [ ] At least 10 sample customers
- [ ] At least 15 sample products across all categories
- [ ] At least 20 sample orders with various statuses
- [ ] At least 10 sample inquiries
- [ ] Data is realistic and representative
- [ ] Script to load sample data is provided

### 4. Stripe Integration (Stubs)
- [ ] Stripe API key configuration (test mode)
- [ ] Create payment intent stub (returns mock success)
- [ ] Process payment stub (simulates successful payment)
- [ ] Webhook handler stub (handles test webhook events)
- [ ] Payment flow documented
- [ ] Clear comments indicating stub vs production code

### 5. Admin Interface
**Authentication**
- [ ] Basic admin login (username/password)
- [ ] Session management
- [ ] Protected admin routes

**Dashboard**
- [ ] Display summary statistics (total customers, orders, revenue)
- [ ] Recent orders list
- [ ] Recent inquiries list
- [ ] Quick action buttons

**Customer Management**
- [ ] List all customers with pagination
- [ ] View customer details
- [ ] View customer order history
- [ ] Search customers by name/email
- [ ] Add/edit customer information

**Product Management**
- [ ] List all products with filtering by category
- [ ] Add new product
- [ ] Edit existing product
- [ ] View product details
- [ ] Track inventory levels

**Order Management**
- [ ] List all orders with filtering by status
- [ ] View order details
- [ ] Update order status
- [ ] View customer information for order
- [ ] Display order items and totals

**Inquiry Management**
- [ ] List all inquiries
- [ ] View inquiry details
- [ ] Mark inquiry as responded/closed
- [ ] Filter by status

### 6. Public Interface Updates
**Contact Form**
- [ ] Save submissions to database (inquiries table)
- [ ] Display success/error messages
- [ ] Email validation
- [ ] Store submission in Firestore for analytics

**Product Catalog** (New)
- [ ] Display products from database
- [ ] Filter by category
- [ ] Show product details page
- [ ] Display price and availability

**Shopping Cart** (Stub)
- [ ] Add items to cart (session-based)
- [ ] View cart contents
- [ ] Update quantities
- [ ] Remove items

**Checkout Flow** (Stub)
- [ ] Customer information form
- [ ] Order summary
- [ ] Stripe payment integration (stub)
- [ ] Create order in database
- [ ] Confirmation page

### 7. Configuration & Deployment
- [ ] Environment variables documented
- [ ] `.env.example` file provided
- [ ] Updated `requirements.txt` with all dependencies
- [ ] Cloud Build configuration supports new dependencies
- [ ] Dockerfile builds successfully
- [ ] Database migrations/initialization handled
- [ ] Connection to danielsbonnin.com project configured

### 8. Testing Requirements
- [ ] All database connections tested
- [ ] CRUD operations verified for each model
- [ ] Sample data loads successfully
- [ ] Admin interface accessible and functional
- [ ] Contact form saves to database
- [ ] Stripe stubs return expected responses
- [ ] Error handling tested (bad inputs, connection failures)

### 9. Documentation
- [ ] README updated with CRM features
- [ ] Environment setup instructions
- [ ] Database schema documentation
- [ ] API/endpoint documentation
- [ ] Sample data loading instructions
- [ ] Admin credentials documented
- [ ] Stripe stub usage documented

### 10. Security Requirements
- [ ] No credentials in source code
- [ ] Environment variables for all secrets
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention in forms
- [ ] CSRF protection for forms
- [ ] Admin routes properly secured
- [ ] Input validation on all forms
- [ ] Pass CodeQL security scan

## Technical Specifications

### Technology Stack
- **Backend**: Flask (Python 3.11)
- **Database**: Google Cloud SQL (PostgreSQL 14+)
- **NoSQL**: Google Firestore
- **Payments**: Stripe (Test Mode Stubs)
- **Deployment**: Google Cloud Run
- **Container**: Docker

### Database Schema

#### Customers Table
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

#### Products Table
```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    image_url VARCHAR(500),
    stock_quantity INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Orders Table
```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    status VARCHAR(50) NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    stripe_payment_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Order Items Table
```sql
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    price_at_purchase DECIMAL(10, 2) NOT NULL
);
```

#### Inquiries Table
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

### Firestore Collections
- **activity_logs**: User activity tracking
- **analytics**: Page views, interactions
- **sessions**: User session data

### Environment Variables Required
```
# Database
DB_HOST=<cloud-sql-connection-name>
DB_NAME=crocheted_crumb
DB_USER=<database-user>
DB_PASSWORD=<database-password>
DB_PORT=5432

# Firestore
GOOGLE_CLOUD_PROJECT=danielsbonnin-com
FIRESTORE_COLLECTION_PREFIX=sarah_site_

# Stripe (Test Mode)
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Admin
ADMIN_USERNAME=admin
ADMIN_PASSWORD=<secure-password>
SECRET_KEY=<flask-secret-key>

# Environment
FLASK_ENV=production
```

## Success Metrics
1. All acceptance criteria marked as complete
2. Sample data successfully loaded
3. Admin can perform all CRM operations
4. Contact form submissions save to database
5. Zero security vulnerabilities in CodeQL scan
6. Code review passes with no critical issues
7. Application successfully deploys to Cloud Run
8. All database connections functional in production

## Out of Scope (Future Enhancements)
- Email notifications
- Advanced analytics dashboard
- Product image uploads
- Real Stripe payment processing (stubs only for now)
- Customer portal
- Inventory management alerts
- Order tracking
- Multi-user admin system
- API endpoints for mobile app
