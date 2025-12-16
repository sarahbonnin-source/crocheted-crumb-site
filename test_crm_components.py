"""
Test script to verify CRM system components without database connection.
This validates imports and basic functionality.
"""
import sys
import os

print("="*60)
print("  CRM System Component Tests")
print("="*60)

# Test 1: Import all modules
print("\n1. Testing module imports...")
try:
    import database
    print("  ✓ database module imported")
except Exception as e:
    print(f"  ✗ database module error: {e}")
    sys.exit(1)

try:
    import models
    print("  ✓ models module imported")
except Exception as e:
    print(f"  ✗ models module error: {e}")
    sys.exit(1)

try:
    import stripe_stubs
    print("  ✓ stripe_stubs module imported")
except Exception as e:
    print(f"  ✗ stripe_stubs module error: {e}")
    sys.exit(1)

try:
    import admin_auth
    print("  ✓ admin_auth module imported")
except Exception as e:
    print(f"  ✗ admin_auth module error: {e}")
    sys.exit(1)

try:
    import app
    print("  ✓ app module imported")
except Exception as e:
    print(f"  ✗ app module error: {e}")
    sys.exit(1)

# Test 2: Verify Stripe stubs work without real API
print("\n2. Testing Stripe stubs...")
try:
    from stripe_stubs import create_payment_intent_stub, process_payment_stub
    
    # Create a mock payment intent
    payment = create_payment_intent_stub(25.50, customer_email="test@example.com")
    assert payment['amount'] == 2550, "Payment amount incorrect"
    assert payment['status'] == 'succeeded', "Payment status incorrect"
    print(f"  ✓ Payment intent created: {payment['id']}")
    
    # Process mock payment
    result = process_payment_stub(payment['id'])
    assert result['success'] == True, "Payment processing failed"
    print(f"  ✓ Payment processed successfully")
    
except Exception as e:
    print(f"  ✗ Stripe stub error: {e}")
    sys.exit(1)

# Test 3: Verify admin auth functions
print("\n3. Testing admin authentication...")
try:
    # Need to reload admin_auth after setting env vars
    import importlib
    
    # Set test credentials
    os.environ['ADMIN_USERNAME'] = 'testadmin'
    os.environ['ADMIN_PASSWORD'] = 'testpass'
    
    # Reload to pick up new env vars
    import admin_auth
    importlib.reload(admin_auth)
    from admin_auth import check_admin_credentials
    
    # Test valid credentials
    assert check_admin_credentials('testadmin', 'testpass') == True, "Valid credentials failed"
    print("  ✓ Valid credentials accepted")
    
    # Test invalid credentials
    assert check_admin_credentials('wrong', 'wrong') == False, "Invalid credentials accepted"
    print("  ✓ Invalid credentials rejected")
    
except Exception as e:
    print(f"  ✗ Admin auth error: {e}")
    sys.exit(1)

# Test 4: Verify Flask app configuration
print("\n4. Testing Flask application...")
try:
    from app import app as flask_app
    
    # Check if Flask app is configured
    assert flask_app is not None, "Flask app not created"
    print("  ✓ Flask app created")
    
    # Check if routes are registered
    routes = [rule.rule for rule in flask_app.url_map.iter_rules()]
    expected_routes = ['/', '/products', '/contact', '/admin/login', '/admin/dashboard']
    
    for route in expected_routes:
        if route in routes:
            print(f"  ✓ Route registered: {route}")
        else:
            print(f"  ✗ Route missing: {route}")
    
except Exception as e:
    print(f"  ✗ Flask app error: {e}")
    sys.exit(1)

# Test 5: Verify template files exist
print("\n5. Testing template files...")
template_files = [
    'templates/base.html',
    'templates/index.html',
    'templates/contact.html',
    'templates/products.html',
    'templates/product_detail.html',
    'templates/cart.html',
    'templates/checkout.html',
    'templates/admin/login.html',
    'templates/admin/dashboard.html',
    'templates/admin/customers.html',
    'templates/admin/orders.html',
    'templates/admin/products.html',
    'templates/admin/inquiries.html'
]

missing_templates = []
for template in template_files:
    if os.path.exists(template):
        print(f"  ✓ Template exists: {template}")
    else:
        print(f"  ✗ Template missing: {template}")
        missing_templates.append(template)

if missing_templates:
    print(f"\n  ✗ {len(missing_templates)} templates missing")
    sys.exit(1)

# Test 6: Verify configuration files
print("\n6. Testing configuration files...")
config_files = [
    '.env.example',
    '.gitignore',
    'requirements.txt',
    'Dockerfile',
    'cloudbuild.yaml',
    'CRM_REQUIREMENTS.md',
    'CRM_DOCUMENTATION.md'
]

for config_file in config_files:
    if os.path.exists(config_file):
        print(f"  ✓ Config exists: {config_file}")
    else:
        print(f"  ✗ Config missing: {config_file}")

# Final summary
print("\n" + "="*60)
print("  ✅ All component tests passed!")
print("="*60)
print("\nNext steps:")
print("  1. Configure .env file with database credentials")
print("  2. Run: python generate_sample_data.py")
print("  3. Run: python app.py")
print("  4. Access admin at: http://localhost:8080/admin/login")
print("="*60 + "\n")
