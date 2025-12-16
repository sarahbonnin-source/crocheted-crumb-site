"""
Generate sample data for the CRM system.
This script populates the database with realistic test data.
"""
import random
from datetime import datetime, timedelta
from database import init_db_pool, init_database_schema, close_db_pool
from models import Customer, Product, Order, OrderItem, Inquiry


# Sample data
FIRST_NAMES = ['Emma', 'Olivia', 'Ava', 'Sophia', 'Isabella', 'Mia', 'Charlotte', 'Amelia', 
               'Liam', 'Noah', 'Oliver', 'James', 'Elijah', 'William', 'Henry', 'Lucas']
LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
              'Rodriguez', 'Martinez', 'Anderson', 'Taylor', 'Thomas', 'Moore', 'Jackson', 'White']

PRODUCT_CATEGORIES = ['plushies', 'wearables', 'home_decor', 'custom']

PRODUCTS_DATA = [
    # Plushies
    ('Adorable Crochet Bunny', 'Soft and cuddly handmade bunny plushie with floppy ears', 35.00, 'plushies', 10),
    ('Tiny Elephant Amigurumi', 'Cute mini elephant perfect for desk decoration', 25.00, 'plushies', 15),
    ('Cozy Bear Plush', 'Large huggable bear made with premium yarn', 45.00, 'plushies', 8),
    ('Rainbow Octopus', 'Colorful octopus with bendy tentacles', 30.00, 'plushies', 12),
    ('Mini Bee Collection', 'Set of 3 tiny bee amigurumi', 20.00, 'plushies', 20),
    
    # Wearables
    ('Chunky Knit Beanie', 'Warm winter beanie in various colors', 28.00, 'wearables', 25),
    ('Infinity Scarf', 'Soft infinity scarf in neutral tones', 35.00, 'wearables', 15),
    ('Fingerless Gloves', 'Cozy fingerless gloves perfect for texting', 22.00, 'wearables', 18),
    ('Baby Booties', 'Adorable crochet booties for newborns', 18.00, 'wearables', 30),
    ('Cable Knit Headband', 'Stylish cable pattern headband', 20.00, 'wearables', 20),
    
    # Home Decor
    ('Boho Wall Hanging', 'Macrame-style wall decoration', 55.00, 'home_decor', 6),
    ('Coaster Set', 'Set of 4 colorful coasters', 15.00, 'home_decor', 40),
    ('Decorative Pillow Cover', 'Textured crochet pillow cover 16x16"', 32.00, 'home_decor', 10),
    ('Plant Hanger', 'Hanging planter for small pots', 25.00, 'home_decor', 12),
    ('Table Runner', 'Elegant lace-pattern table runner', 48.00, 'home_decor', 5),
]

ORDER_STATUSES = ['pending', 'paid', 'processing', 'shipped', 'delivered']

INQUIRY_MESSAGES = [
    "Hi! I'd love to order a custom bunny in pink. Is that possible?",
    "Do you ship internationally? I'm in Canada.",
    "Can I get the baby booties in blue instead of the colors shown?",
    "I'm interested in a custom order for a wedding gift. Can we discuss?",
    "How long does shipping usually take?",
    "Are your products machine washable?",
    "I received my order and it's beautiful! Thank you so much!",
    "Can you make a custom plushie of my dog?",
    "What's the return policy if the size doesn't fit?",
    "Do you offer gift wrapping services?",
]


def generate_sample_customers(count=10):
    """Generate sample customer data."""
    print(f"\n📝 Generating {count} sample customers...")
    customer_ids = []
    
    for i in range(count):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        name = f"{first_name} {last_name}"
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@example.com"
        phone = f"+1{random.randint(200, 999)}{random.randint(100, 999)}{random.randint(1000, 9999)}"
        address = f"{random.randint(100, 9999)} Main St, City, State {random.randint(10000, 99999)}"
        
        customer_id = Customer.create(name, email, phone, address)
        if customer_id:
            customer_ids.append(customer_id)
            print(f"  ✓ Created customer: {name} ({email})")
        else:
            print(f"  ✗ Failed to create customer: {name}")
    
    print(f"✓ Created {len(customer_ids)} customers")
    return customer_ids


def generate_sample_products():
    """Generate sample product data."""
    print(f"\n📦 Generating {len(PRODUCTS_DATA)} sample products...")
    product_ids = []
    
    for name, description, price, category, stock in PRODUCTS_DATA:
        # Use placeholder image URL
        image_url = f"https://placehold.co/400x400/E8D5C4/8B7355?text={name.replace(' ', '+')}"
        
        product_id = Product.create(name, description, price, category, image_url, stock)
        if product_id:
            product_ids.append(product_id)
            print(f"  ✓ Created product: {name} (${price})")
        else:
            print(f"  ✗ Failed to create product: {name}")
    
    print(f"✓ Created {len(product_ids)} products")
    return product_ids


def generate_sample_orders(customer_ids, product_ids, count=20):
    """Generate sample order data."""
    print(f"\n🛍️  Generating {count} sample orders...")
    order_ids = []
    
    for i in range(count):
        # Pick a random customer
        customer_id = random.choice(customer_ids)
        
        # Pick 1-4 random products
        num_items = random.randint(1, 4)
        order_products = random.sample(product_ids, min(num_items, len(product_ids)))
        
        # Calculate total
        total_amount = 0.0
        items_data = []
        
        for product_id in order_products:
            product = Product.get_by_id(product_id)
            if product:
                quantity = random.randint(1, 3)
                price = product['price']
                total_amount += price * quantity
                items_data.append((product_id, quantity, price))
        
        # Create order with random status
        status = random.choice(ORDER_STATUSES)
        stripe_payment_id = f"pi_stub_{random.randint(100000, 999999)}" if status != 'pending' else None
        
        order_id = Order.create(customer_id, total_amount, status, stripe_payment_id)
        if order_id:
            order_ids.append(order_id)
            
            # Create order items
            for product_id, quantity, price in items_data:
                OrderItem.create(order_id, product_id, quantity, price)
            
            customer = Customer.get_by_id(customer_id)
            print(f"  ✓ Created order #{order_id} for {customer['name']} (${total_amount:.2f}, {status})")
        else:
            print(f"  ✗ Failed to create order for customer {customer_id}")
    
    print(f"✓ Created {len(order_ids)} orders")
    return order_ids


def generate_sample_inquiries(count=10):
    """Generate sample inquiry data."""
    print(f"\n💬 Generating {count} sample inquiries...")
    inquiry_ids = []
    
    statuses = ['new', 'new', 'new', 'responded', 'responded', 'closed']  # More "new" inquiries
    
    for i in range(count):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        name = f"{first_name} {last_name}"
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@example.com"
        message = random.choice(INQUIRY_MESSAGES)
        status = random.choice(statuses)
        
        inquiry_id = Inquiry.create(name, email, message, status)
        if inquiry_id:
            inquiry_ids.append(inquiry_id)
            print(f"  ✓ Created inquiry from {name} ({status})")
        else:
            print(f"  ✗ Failed to create inquiry from {name}")
    
    print(f"✓ Created {len(inquiry_ids)} inquiries")
    return inquiry_ids


def main():
    """Main function to generate all sample data."""
    print("\n" + "="*60)
    print("  📊 CRM Sample Data Generator")
    print("="*60)
    
    # Initialize database
    print("\n🔌 Connecting to database...")
    if not init_db_pool():
        print("✗ Failed to connect to database. Check your configuration.")
        return
    
    print("✓ Connected to database")
    
    # Initialize schema
    print("\n🏗️  Initializing database schema...")
    if not init_database_schema():
        print("✗ Failed to initialize database schema")
        close_db_pool()
        return
    
    print("✓ Database schema ready")
    
    # Generate sample data
    try:
        customer_ids = generate_sample_customers(10)
        product_ids = generate_sample_products()
        order_ids = generate_sample_orders(customer_ids, product_ids, 20)
        inquiry_ids = generate_sample_inquiries(10)
        
        print("\n" + "="*60)
        print("  ✅ Sample Data Generation Complete!")
        print("="*60)
        print(f"  Customers: {len(customer_ids)}")
        print(f"  Products:  {len(product_ids)}")
        print(f"  Orders:    {len(order_ids)}")
        print(f"  Inquiries: {len(inquiry_ids)}")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error generating sample data: {e}")
    finally:
        close_db_pool()


if __name__ == '__main__':
    main()
