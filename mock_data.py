"""
Mock data module for frontend development and preview.

This module provides mock data for the frontend to use when the backend
is not connected or when running in preview mode.
"""

# Mock gallery items for the frontend
MOCK_GALLERY_ITEMS = [
    {
        "id": 1,
        "title": "Plushies",
        "description": "Adorable handmade plush toys",
        "color": "#E8D5C4",
        "image_url": None  # Using placeholder for now
    },
    {
        "id": 2,
        "title": "Wearables",
        "description": "Cozy crocheted accessories",
        "color": "#B0C4B1",
        "image_url": None
    },
    {
        "id": 3,
        "title": "Home Decor",
        "description": "Beautiful home decorations",
        "color": "#D7B9B3",
        "image_url": None
    }
]

# Mock site configuration
MOCK_SITE_CONFIG = {
    "site_name": "The Crocheted Crumb",
    "tagline": "Handcrafted with Love",
    "description": "Cozy, cute, and custom crochet creations for you and your loved ones.",
    "contact_email": "snbonnin@gmail.com",
    "year": 2024,
    "artist_name": "Sarah",
    "artist_bio": "Welcome to The Crocheted Crumb! I'm Sarah, and I turn yarn into keepsakes. Every stitch is made with care, patience, and a whole lot of love. Whether you're looking for a unique gift or a treat for yourself, I hope you find something that brings you joy."
}

# Mock contact info
MOCK_CONTACT_INFO = {
    "email": "snbonnin@gmail.com",
    "message": "Email me for any questions, possible product requests, to talk about crocheting, and to possibly order a commission! Thanks for reaching out! -Sarah"
}


def get_gallery_items():
    """Return mock gallery items."""
    return MOCK_GALLERY_ITEMS


def get_site_config():
    """Return mock site configuration."""
    return MOCK_SITE_CONFIG


def get_contact_info():
    """Return mock contact information."""
    return MOCK_CONTACT_INFO
