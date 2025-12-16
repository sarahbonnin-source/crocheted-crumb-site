"""
Database configuration and connection management for Cloud SQL and Firestore.
"""
import os
from typing import Optional
import psycopg2
from psycopg2 import pool
from google.cloud import firestore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', '/cloudsql/danielsbonnin-com:us-central1:postgres'),
    'database': os.getenv('DB_NAME', 'crocheted_crumb'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
    'port': os.getenv('DB_PORT', '5432')
}

# Connection pool
connection_pool: Optional[pool.SimpleConnectionPool] = None

def init_db_pool(minconn=1, maxconn=10):
    """Initialize the database connection pool."""
    global connection_pool
    try:
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            minconn,
            maxconn,
            **DB_CONFIG
        )
        if connection_pool:
            print("✓ Database connection pool created successfully")
            return True
    except Exception as e:
        print(f"✗ Error creating connection pool: {e}")
        connection_pool = None
        return False

def get_db_connection():
    """Get a connection from the pool."""
    if connection_pool:
        try:
            return connection_pool.getconn()
        except Exception as e:
            print(f"Error getting connection from pool: {e}")
            return None
    return None

def return_db_connection(conn):
    """Return a connection to the pool."""
    if connection_pool and conn:
        try:
            connection_pool.putconn(conn)
        except Exception as e:
            print(f"Error returning connection to pool: {e}")

def close_db_pool():
    """Close all connections in the pool."""
    global connection_pool
    if connection_pool:
        connection_pool.closeall()
        print("✓ Database connection pool closed")

# Firestore client
_firestore_client: Optional[firestore.Client] = None

def get_firestore_client():
    """Get or create Firestore client."""
    global _firestore_client
    if _firestore_client is None:
        try:
            project_id = os.getenv('GOOGLE_CLOUD_PROJECT', 'danielsbonnin-com')
            _firestore_client = firestore.Client(project=project_id)
            print("✓ Firestore client initialized successfully")
        except Exception as e:
            print(f"✗ Error initializing Firestore client: {e}")
            _firestore_client = None
    return _firestore_client

def get_firestore_collection(collection_name):
    """Get a Firestore collection with prefix."""
    client = get_firestore_client()
    if client:
        prefix = os.getenv('FIRESTORE_COLLECTION_PREFIX', 'sarah_site_')
        return client.collection(f"{prefix}{collection_name}")
    return None

def init_database_schema():
    """Initialize database schema if it doesn't exist."""
    conn = get_db_connection()
    if not conn:
        print("✗ Cannot initialize schema: no database connection")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Create customers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                phone VARCHAR(50),
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
                category VARCHAR(50) NOT NULL,
                image_url VARCHAR(500),
                stock_quantity INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                customer_id INTEGER REFERENCES customers(id),
                status VARCHAR(50) NOT NULL DEFAULT 'pending',
                total_amount DECIMAL(10, 2) NOT NULL,
                stripe_payment_id VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create order_items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id SERIAL PRIMARY KEY,
                order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
                product_id INTEGER REFERENCES products(id),
                quantity INTEGER NOT NULL CHECK (quantity > 0),
                price_at_purchase DECIMAL(10, 2) NOT NULL
            );
        """)
        
        # Create inquiries table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inquiries (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                message TEXT NOT NULL,
                status VARCHAR(50) DEFAULT 'new',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                responded_at TIMESTAMP
            );
        """)
        
        conn.commit()
        cursor.close()
        print("✓ Database schema initialized successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error initializing database schema: {e}")
        conn.rollback()
        return False
    finally:
        return_db_connection(conn)
