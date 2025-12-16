"""
Admin authentication and session management.
"""
import os
from functools import wraps
from flask import session, redirect, url_for, flash
from dotenv import load_dotenv

load_dotenv()

# Admin credentials from environment variables
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'change_this_password')


def check_admin_credentials(username: str, password: str) -> bool:
    """
    Verify admin credentials.
    
    Args:
        username: Username to check
        password: Password to check
    
    Returns:
        True if credentials are valid, False otherwise
    """
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD


def login_admin(username: str):
    """
    Log in an admin user by setting session variables.
    
    Args:
        username: Admin username
    """
    session['admin_logged_in'] = True
    session['admin_username'] = username


def logout_admin():
    """Log out the admin user by clearing session variables."""
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)


def is_admin_logged_in() -> bool:
    """
    Check if an admin user is currently logged in.
    
    Returns:
        True if admin is logged in, False otherwise
    """
    return session.get('admin_logged_in', False)


def admin_required(f):
    """
    Decorator to require admin authentication for a route.
    
    Usage:
        @app.route('/admin/dashboard')
        @admin_required
        def admin_dashboard():
            return render_template('admin/dashboard.html')
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_admin_logged_in():
            flash('Please log in to access the admin area.', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function
