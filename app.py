import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from dotenv import load_dotenv
from google.cloud import firestore
from database import init_db_pool, init_database_schema, close_db_pool, get_firestore_collection
from models import Customer, Product, Order, OrderItem, Inquiry
from admin_auth import check_admin_credentials, login_admin, logout_admin, admin_required
from stripe_stubs import create_payment_intent_stub, process_payment_stub, STRIPE_PUBLIC_KEY
import atexit

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize database on startup
@app.before_first_request
def initialize():
    """Initialize database connection and schema."""
    print("Initializing CRM system...")
    init_db_pool()
    init_database_schema()

# Close database pool on shutdown
atexit.register(close_db_pool)


# ============================================================================
# Public Routes
# ============================================================================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/products")
def products():
    """Display product catalog."""
    category = request.args.get('category')
    products_list = Product.get_all(category=category, limit=50)
    categories = ['plushies', 'wearables', 'home_decor', 'custom']
    return render_template("products.html", products=products_list, 
                         categories=categories, selected_category=category)


@app.route("/products/<int:product_id>")
def product_detail(product_id):
    """Display product detail page."""
    product = Product.get_by_id(product_id)
    if not product:
        flash("Product not found", "error")
        return redirect(url_for('products'))
    return render_template("product_detail.html", product=product)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Contact form - saves inquiries to database."""
    if request.method == "POST":
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()
        
        # Validate inputs
        if not name or not email or not message:
            flash("Please fill in all fields", "error")
            return render_template("contact.html")
        
        # Save inquiry to database
        inquiry_id = Inquiry.create(name, email, message)
        
        if inquiry_id:
            # Also log to Firestore for analytics
            try:
                firestore_collection = get_firestore_collection('inquiries')
                if firestore_collection:
                    firestore_collection.add({
                        'inquiry_id': inquiry_id,
                        'name': name,
                        'email': email,
                        'timestamp': firestore.SERVER_TIMESTAMP
                    })
            except Exception as e:
                print(f"Firestore logging error: {e}")
            
            flash("Thank you for your message! We'll get back to you soon.", "success")
            return redirect(url_for('contact'))
        else:
            flash("Sorry, there was an error submitting your message. Please try again.", "error")
    
    return render_template("contact.html")


@app.route("/cart")
def cart():
    """View shopping cart."""
    cart_items = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template("cart.html", cart_items=cart_items, total=total)


@app.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    """Add product to cart."""
    product = Product.get_by_id(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    quantity = int(request.form.get('quantity', 1))
    
    # Get or create cart in session
    cart = session.get('cart', [])
    
    # Check if product already in cart
    found = False
    for item in cart:
        if item['product_id'] == product_id:
            item['quantity'] += quantity
            found = True
            break
    
    if not found:
        cart.append({
            'product_id': product_id,
            'name': product['name'],
            'price': product['price'],
            'quantity': quantity,
            'image_url': product['image_url']
        })
    
    session['cart'] = cart
    flash(f"Added {product['name']} to cart!", "success")
    return redirect(url_for('products'))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    """Checkout process (stub with Stripe)."""
    cart_items = session.get('cart', [])
    if not cart_items:
        flash("Your cart is empty", "warning")
        return redirect(url_for('products'))
    
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    
    if request.method == "POST":
        # Get customer information
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        
        if not name or not email:
            flash("Please fill in required fields", "error")
            return render_template("checkout.html", cart_items=cart_items, total=total)
        
        # Create or get customer
        customer = Customer.get_by_email(email)
        if customer:
            customer_id = customer['id']
        else:
            customer_id = Customer.create(name, email, phone, address)
        
        if not customer_id:
            flash("Error creating customer record", "error")
            return render_template("checkout.html", cart_items=cart_items, total=total)
        
        # Create payment intent (stub)
        payment_intent = create_payment_intent_stub(total, customer_email=email)
        
        # Create order
        order_id = Order.create(customer_id, total, status='paid', 
                               stripe_payment_id=payment_intent['id'])
        
        if order_id:
            # Create order items
            for item in cart_items:
                OrderItem.create(order_id, item['product_id'], 
                               item['quantity'], item['price'])
            
            # Clear cart
            session['cart'] = []
            
            flash("Order placed successfully! (STUB: No real payment processed)", "success")
            return redirect(url_for('order_confirmation', order_id=order_id))
        else:
            flash("Error creating order", "error")
    
    return render_template("checkout.html", cart_items=cart_items, total=total,
                         stripe_public_key=STRIPE_PUBLIC_KEY)


@app.route("/order/<int:order_id>")
def order_confirmation(order_id):
    """Order confirmation page."""
    order = Order.get_by_id(order_id)
    if not order:
        flash("Order not found", "error")
        return redirect(url_for('index'))
    
    order_items = OrderItem.get_order_items(order_id)
    return render_template("order_confirmation.html", order=order, items=order_items)


# ============================================================================
# Admin Routes
# ============================================================================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """Admin login page."""
    if request.method == "POST":
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if check_admin_credentials(username, password):
            login_admin(username)
            flash("Logged in successfully!", "success")
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid credentials", "error")
    
    return render_template("admin/login.html")


@app.route("/admin/logout")
def admin_logout():
    """Admin logout."""
    logout_admin()
    flash("Logged out successfully", "success")
    return redirect(url_for('index'))


@app.route("/admin")
@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    """Admin dashboard."""
    # Get summary statistics
    customers = Customer.get_all(limit=1000)
    orders = Order.get_all(limit=1000)
    products = Product.get_all(limit=1000)
    inquiries = Inquiry.get_all(limit=1000)
    
    total_revenue = sum(order['total_amount'] for order in orders if order['status'] in ['paid', 'processing', 'shipped', 'delivered'])
    
    recent_orders = Order.get_all(limit=10)
    recent_inquiries = Inquiry.get_all(status='new', limit=10)
    
    stats = {
        'total_customers': len(customers),
        'total_orders': len(orders),
        'total_products': len(products),
        'total_inquiries': len(inquiries),
        'total_revenue': total_revenue,
        'new_inquiries': len([i for i in inquiries if i['status'] == 'new'])
    }
    
    return render_template("admin/dashboard.html", stats=stats,
                         recent_orders=recent_orders,
                         recent_inquiries=recent_inquiries)


@app.route("/admin/customers")
@admin_required
def admin_customers():
    """Admin customer management."""
    search = request.args.get('search', '')
    if search:
        customers = Customer.search(search)
    else:
        customers = Customer.get_all(limit=100)
    return render_template("admin/customers.html", customers=customers, search=search)


@app.route("/admin/customers/<int:customer_id>")
@admin_required
def admin_customer_detail(customer_id):
    """Admin customer detail page."""
    customer = Customer.get_by_id(customer_id)
    if not customer:
        flash("Customer not found", "error")
        return redirect(url_for('admin_customers'))
    
    orders = Order.get_customer_orders(customer_id)
    return render_template("admin/customer_detail.html", customer=customer, orders=orders)


@app.route("/admin/products")
@admin_required
def admin_products():
    """Admin product management."""
    category = request.args.get('category')
    products_list = Product.get_all(category=category, limit=100)
    categories = ['plushies', 'wearables', 'home_decor', 'custom']
    return render_template("admin/products.html", products=products_list,
                         categories=categories, selected_category=category)


@app.route("/admin/products/<int:product_id>")
@admin_required
def admin_product_detail(product_id):
    """Admin product detail page."""
    product = Product.get_by_id(product_id)
    if not product:
        flash("Product not found", "error")
        return redirect(url_for('admin_products'))
    return render_template("admin/product_detail.html", product=product)


@app.route("/admin/orders")
@admin_required
def admin_orders():
    """Admin order management."""
    status = request.args.get('status')
    orders = Order.get_all(status=status, limit=100)
    statuses = ['pending', 'paid', 'processing', 'shipped', 'delivered', 'cancelled']
    return render_template("admin/orders.html", orders=orders,
                         statuses=statuses, selected_status=status)


@app.route("/admin/orders/<int:order_id>")
@admin_required
def admin_order_detail(order_id):
    """Admin order detail page."""
    order = Order.get_by_id(order_id)
    if not order:
        flash("Order not found", "error")
        return redirect(url_for('admin_orders'))
    
    items = OrderItem.get_order_items(order_id)
    customer = Customer.get_by_id(order['customer_id'])
    return render_template("admin/order_detail.html", order=order, items=items, customer=customer)


@app.route("/admin/orders/<int:order_id>/update-status", methods=["POST"])
@admin_required
def admin_update_order_status(order_id):
    """Update order status."""
    new_status = request.form.get('status')
    if Order.update_status(order_id, new_status):
        flash("Order status updated successfully", "success")
    else:
        flash("Error updating order status", "error")
    return redirect(url_for('admin_order_detail', order_id=order_id))


@app.route("/admin/inquiries")
@admin_required
def admin_inquiries():
    """Admin inquiry management."""
    status = request.args.get('status')
    inquiries = Inquiry.get_all(status=status, limit=100)
    statuses = ['new', 'responded', 'closed']
    return render_template("admin/inquiries.html", inquiries=inquiries,
                         statuses=statuses, selected_status=status)


@app.route("/admin/inquiries/<int:inquiry_id>")
@admin_required
def admin_inquiry_detail(inquiry_id):
    """Admin inquiry detail page."""
    inquiry = Inquiry.get_by_id(inquiry_id)
    if not inquiry:
        flash("Inquiry not found", "error")
        return redirect(url_for('admin_inquiries'))
    return render_template("admin/inquiry_detail.html", inquiry=inquiry)


@app.route("/admin/inquiries/<int:inquiry_id>/update-status", methods=["POST"])
@admin_required
def admin_update_inquiry_status(inquiry_id):
    """Update inquiry status."""
    new_status = request.form.get('status')
    if Inquiry.update_status(inquiry_id, new_status):
        flash("Inquiry status updated successfully", "success")
    else:
        flash("Error updating inquiry status", "error")
    return redirect(url_for('admin_inquiry_detail', inquiry_id=inquiry_id))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
