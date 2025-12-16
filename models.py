"""
Data models and CRUD operations for CRM system.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from database import get_db_connection, return_db_connection


class Customer:
    """Customer model and CRUD operations."""
    
    @staticmethod
    def create(name: str, email: str, phone: str = None, address: str = None) -> Optional[int]:
        """Create a new customer."""
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO customers (name, email, phone, address)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (name, email, phone, address)
            )
            customer_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            return customer_id
        except Exception as e:
            print(f"Error creating customer: {e}")
            conn.rollback()
            return None
        finally:
            return_db_connection(conn)
    
    @staticmethod
    def get_by_id(customer_id: int) -> Optional[Dict[str, Any]]:
        """Get customer by ID."""
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, name, email, phone, address, created_at, updated_at
                FROM customers WHERE id = %s
                """,
                (customer_id,)
            )
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return {
                    'id': row[0],
                    'name': row[1],
                    'email': row[2],
                    'phone': row[3],
                    'address': row[4],
                    'created_at': row[5],
                    'updated_at': row[6]
                }
            return None
        except Exception as e:
            print(f"Error getting customer: {e}")
            return None
        finally:
            return_db_connection(conn)
    
    @staticmethod
    def get_by_email(email: str) -> Optional[Dict[str, Any]]:
        """Get customer by email."""
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, name, email, phone, address, created_at, updated_at
                FROM customers WHERE email = %s
                """,
                (email,)
            )
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return {
                    'id': row[0],
                    'name': row[1],
                    'email': row[2],
                    'phone': row[3],
                    'address': row[4],
                    'created_at': row[5],
                    'updated_at': row[6]
                }
            return None
        except Exception as e:
            print(f"Error getting customer by email: {e}")
            return None
        finally:
            return_db_connection(conn)
    
    @staticmethod
    def get_all(limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all customers with pagination."""
        conn = get_db_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, name, email, phone, address, created_at, updated_at
                FROM customers
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
                """,
                (limit, offset)
            )
            rows = cursor.fetchall()
            cursor.close()
            
            customers = []
            for row in rows:
                customers.append({
                    'id': row[0],
                    'name': row[1],
                    'email': row[2],
                    'phone': row[3],
                    'address': row[4],
                    'created_at': row[5],
                    'updated_at': row[6]
                })
            return customers
        except Exception as e:
            print(f"Error getting all customers: {e}")
            return []
        finally:
            return_db_connection(conn)
    
    @staticmethod
    def update(customer_id: int, name: str = None, email: str = None, 
               phone: str = None, address: str = None) -> bool:
        """Update customer information."""
        conn = get_db_connection()
        if not conn:
            return False
        
        try:
            updates = []
            params = []
            
            if name is not None:
                updates.append("name = %s")
                params.append(name)
            if email is not None:
                updates.append("email = %s")
                params.append(email)
            if phone is not None:
                updates.append("phone = %s")
                params.append(phone)
            if address is not None:
                updates.append("address = %s")
                params.append(address)
            
            if not updates:
                return False
            
            updates.append("updated_at = CURRENT_TIMESTAMP")
            params.append(customer_id)
            
            cursor = conn.cursor()
            cursor.execute(
                f"""
                UPDATE customers
                SET {', '.join(updates)}
                WHERE id = %s
                """,
                params
            )
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error updating customer: {e}")
            conn.rollback()
            return False
        finally:
            return_db_connection(conn)
    
    @staticmethod
    def search(query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Search customers by name or email."""
        conn = get_db_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            search_pattern = f"%{query}%"
            cursor.execute(
                """
                SELECT id, name, email, phone, address, created_at, updated_at
                FROM customers
                WHERE name ILIKE %s OR email ILIKE %s
                ORDER BY created_at DESC
                LIMIT %s
                """,
                (search_pattern, search_pattern, limit)
            )
            rows = cursor.fetchall()
            cursor.close()
            
            customers = []
            for row in rows:
                customers.append({
                    'id': row[0],
                    'name': row[1],
                    'email': row[2],
                    'phone': row[3],
                    'address': row[4],
                    'created_at': row[5],
                    'updated_at': row[6]
                })
            return customers
        except Exception as e:
            print(f"Error searching customers: {e}")
            return []
        finally:
            return_db_connection(conn)


class Product:
    """Product model and CRUD operations."""
    
    @staticmethod
    def create(name: str, description: str, price: float, category: str,
               image_url: str = None, stock_quantity: int = 0) -> Optional[int]:
        """Create a new product."""
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO products (name, description, price, category, image_url, stock_quantity)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (name, description, price, category, image_url, stock_quantity)
            )
            product_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            return product_id
        except Exception as e:
            print(f"Error creating product: {e}")
            conn.rollback()
            return None
        finally:
            return_db_connection(conn)
    
    @staticmethod
    def get_by_id(product_id: int) -> Optional[Dict[str, Any]]:
        """Get product by ID."""
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, name, description, price, category, image_url, stock_quantity, created_at
                FROM products WHERE id = %s
                """,
                (product_id,)
            )
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return {
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'price': float(row[3]),
                    'category': row[4],
                    'image_url': row[5],
                    'stock_quantity': row[6],
                    'created_at': row[7]
                }
            return None
        except Exception as e:
            print(f"Error getting product: {e}")
            return None
        finally:
            return_db_connection(conn)
    
    @staticmethod
    def get_all(category: str = None, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all products with optional category filter."""
        conn = get_db_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            if category:
                cursor.execute(
                    """
                    SELECT id, name, description, price, category, image_url, stock_quantity, created_at
                    FROM products
                    WHERE category = %s
                    ORDER BY created_at DESC
                    LIMIT %s OFFSET %s
                    """,
                    (category, limit, offset)
                )
            else:
                cursor.execute(
                    """
                    SELECT id, name, description, price, category, image_url, stock_quantity, created_at
                    FROM products
                    ORDER BY created_at DESC
                    LIMIT %s OFFSET %s
                    """,
                    (limit, offset)
                )
            rows = cursor.fetchall()
            cursor.close()
            
            products = []
            for row in rows:
                products.append({
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'price': float(row[3]),
                    'category': row[4],
                    'image_url': row[5],
                    'stock_quantity': row[6],
                    'created_at': row[7]
                })
            return products
        except Exception as e:
            print(f"Error getting all products: {e}")
            return []
        finally:
            return_db_connection(conn)
    
    @staticmethod
    def update(product_id: int, name: str = None, description: str = None,
               price: float = None, category: str = None, image_url: str = None,
               stock_quantity: int = None) -> bool:
        """Update product information."""
        conn = get_db_connection()
        if not conn:
            return False
        
        try:
            updates = []
            params = []
            
            if name is not None:
                updates.append("name = %s")
                params.append(name)
            if description is not None:
                updates.append("description = %s")
                params.append(description)
            if price is not None:
                updates.append("price = %s")
                params.append(price)
            if category is not None:
                updates.append("category = %s")
                params.append(category)
            if image_url is not None:
                updates.append("image_url = %s")
                params.append(image_url)
            if stock_quantity is not None:
                updates.append("stock_quantity = %s")
                params.append(stock_quantity)
            
            if not updates:
                return False
            
            params.append(product_id)
            
            cursor = conn.cursor()
            cursor.execute(
                f"""
                UPDATE products
                SET {', '.join(updates)}
                WHERE id = %s
                """,
                params
            )
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error updating product: {e}")
            conn.rollback()
            return False
        finally:
            return_db_connection(conn)


class Order:
    """Order model and CRUD operations."""
    
    @staticmethod
    def create(customer_id: int, total_amount: float, status: str = 'pending',
               stripe_payment_id: str = None) -> Optional[int]:
        """Create a new order."""
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO orders (customer_id, total_amount, status, stripe_payment_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (customer_id, total_amount, status, stripe_payment_id)
            )
            order_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            return order_id
        except Exception as e:
            print(f"Error creating order: {e}")
            conn.rollback()
            return None
        finally:
            return_db_connection(conn)
    
    @staticmethod
    def get_by_id(order_id: int) -> Optional[Dict[str, Any]]:
        """Get order by ID."""
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT o.id, o.customer_id, o.status, o.total_amount, o.stripe_payment_id,
                       o.created_at, o.updated_at, c.name, c.email
                FROM orders o
                LEFT JOIN customers c ON o.customer_id = c.id
                WHERE o.id = %s
                """,
                (order_id,)
            )
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return {
                    'id': row[0],
                    'customer_id': row[1],
                    'status': row[2],
                    'total_amount': float(row[3]),
                    'stripe_payment_id': row[4],
                    'created_at': row[5],
                    'updated_at': row[6],
                    'customer_name': row[7],
                    'customer_email': row[8]
                }
            return None
        except Exception as e:
            print(f"Error getting order: {e}")
            return None
        finally:
            return_db_connection(conn)
    
    @staticmethod
    def get_all(status: str = None, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all orders with optional status filter."""
        conn = get_db_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            if status:
                cursor.execute(
                    """
                    SELECT o.id, o.customer_id, o.status, o.total_amount, o.stripe_payment_id,
                           o.created_at, o.updated_at, c.name, c.email
                    FROM orders o
                    LEFT JOIN customers c ON o.customer_id = c.id
                    WHERE o.status = %s
                    ORDER BY o.created_at DESC
                    LIMIT %s OFFSET %s
                    """,
                    (status, limit, offset)
                )
            else:
                cursor.execute(
                    """
                    SELECT o.id, o.customer_id, o.status, o.total_amount, o.stripe_payment_id,
                           o.created_at, o.updated_at, c.name, c.email
                    FROM orders o
                    LEFT JOIN customers c ON o.customer_id = c.id
                    ORDER BY o.created_at DESC
                    LIMIT %s OFFSET %s
                    """,
                    (limit, offset)
                )
            rows = cursor.fetchall()
            cursor.close()
            
            orders = []
            for row in rows:
                orders.append({
                    'id': row[0],
                    'customer_id': row[1],
                    'status': row[2],
                    'total_amount': float(row[3]),
                    'stripe_payment_id': row[4],
                    'created_at': row[5],
                    'updated_at': row[6],
                    'customer_name': row[7],
                    'customer_email': row[8]
                })
            return orders
        except Exception as e:
            print(f"Error getting all orders: {e}")
            return []
        finally:
            return_db_connection(conn)
    
    @staticmethod
    def update_status(order_id: int, status: str) -> bool:
        """Update order status."""
        conn = get_db_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE orders
                SET status = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                """,
                (status, order_id)
            )
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error updating order status: {e}")
            conn.rollback()
            return False
        finally:
            return_db_connection(conn)
    
    @staticmethod
    def get_customer_orders(customer_id: int) -> List[Dict[str, Any]]:
        """Get all orders for a specific customer."""
        conn = get_db_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, customer_id, status, total_amount, stripe_payment_id,
                       created_at, updated_at
                FROM orders
                WHERE customer_id = %s
                ORDER BY created_at DESC
                """,
                (customer_id,)
            )
            rows = cursor.fetchall()
            cursor.close()
            
            orders = []
            for row in rows:
                orders.append({
                    'id': row[0],
                    'customer_id': row[1],
                    'status': row[2],
                    'total_amount': float(row[3]),
                    'stripe_payment_id': row[4],
                    'created_at': row[5],
                    'updated_at': row[6]
                })
            return orders
        except Exception as e:
            print(f"Error getting customer orders: {e}")
            return []
        finally:
            return_db_connection(conn)


class OrderItem:
    """Order item model and CRUD operations."""
    
    @staticmethod
    def create(order_id: int, product_id: int, quantity: int, price_at_purchase: float) -> Optional[int]:
        """Create a new order item."""
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (order_id, product_id, quantity, price_at_purchase)
            )
            item_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            return item_id
        except Exception as e:
            print(f"Error creating order item: {e}")
            conn.rollback()
            return None
        finally:
            return_db_connection(conn)
    
    @staticmethod
    def get_order_items(order_id: int) -> List[Dict[str, Any]]:
        """Get all items for an order."""
        conn = get_db_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT oi.id, oi.order_id, oi.product_id, oi.quantity, oi.price_at_purchase,
                       p.name, p.description, p.image_url
                FROM order_items oi
                LEFT JOIN products p ON oi.product_id = p.id
                WHERE oi.order_id = %s
                """,
                (order_id,)
            )
            rows = cursor.fetchall()
            cursor.close()
            
            items = []
            for row in rows:
                items.append({
                    'id': row[0],
                    'order_id': row[1],
                    'product_id': row[2],
                    'quantity': row[3],
                    'price_at_purchase': float(row[4]),
                    'product_name': row[5],
                    'product_description': row[6],
                    'product_image_url': row[7]
                })
            return items
        except Exception as e:
            print(f"Error getting order items: {e}")
            return []
        finally:
            return_db_connection(conn)


class Inquiry:
    """Inquiry/Contact model and CRUD operations."""
    
    @staticmethod
    def create(name: str, email: str, message: str, status: str = 'new') -> Optional[int]:
        """Create a new inquiry."""
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO inquiries (name, email, message, status)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (name, email, message, status)
            )
            inquiry_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            return inquiry_id
        except Exception as e:
            print(f"Error creating inquiry: {e}")
            conn.rollback()
            return None
        finally:
            return_db_connection(conn)
    
    @staticmethod
    def get_by_id(inquiry_id: int) -> Optional[Dict[str, Any]]:
        """Get inquiry by ID."""
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, name, email, message, status, created_at, responded_at
                FROM inquiries WHERE id = %s
                """,
                (inquiry_id,)
            )
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return {
                    'id': row[0],
                    'name': row[1],
                    'email': row[2],
                    'message': row[3],
                    'status': row[4],
                    'created_at': row[5],
                    'responded_at': row[6]
                }
            return None
        except Exception as e:
            print(f"Error getting inquiry: {e}")
            return None
        finally:
            return_db_connection(conn)
    
    @staticmethod
    def get_all(status: str = None, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all inquiries with optional status filter."""
        conn = get_db_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            if status:
                cursor.execute(
                    """
                    SELECT id, name, email, message, status, created_at, responded_at
                    FROM inquiries
                    WHERE status = %s
                    ORDER BY created_at DESC
                    LIMIT %s OFFSET %s
                    """,
                    (status, limit, offset)
                )
            else:
                cursor.execute(
                    """
                    SELECT id, name, email, message, status, created_at, responded_at
                    FROM inquiries
                    ORDER BY created_at DESC
                    LIMIT %s OFFSET %s
                    """,
                    (limit, offset)
                )
            rows = cursor.fetchall()
            cursor.close()
            
            inquiries = []
            for row in rows:
                inquiries.append({
                    'id': row[0],
                    'name': row[1],
                    'email': row[2],
                    'message': row[3],
                    'status': row[4],
                    'created_at': row[5],
                    'responded_at': row[6]
                })
            return inquiries
        except Exception as e:
            print(f"Error getting all inquiries: {e}")
            return []
        finally:
            return_db_connection(conn)
    
    @staticmethod
    def update_status(inquiry_id: int, status: str) -> bool:
        """Update inquiry status."""
        conn = get_db_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            if status == 'responded' or status == 'closed':
                cursor.execute(
                    """
                    UPDATE inquiries
                    SET status = %s, responded_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                    """,
                    (status, inquiry_id)
                )
            else:
                cursor.execute(
                    """
                    UPDATE inquiries
                    SET status = %s
                    WHERE id = %s
                    """,
                    (status, inquiry_id)
                )
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error updating inquiry status: {e}")
            conn.rollback()
            return False
        finally:
            return_db_connection(conn)
