import os
from flask import Flask, render_template

from mock_data import get_gallery_items, get_site_config, get_contact_info

app = Flask(__name__)

# Enable mock data mode via environment variable (default: True for development)
MOCK_MODE = os.environ.get("MOCK_MODE", "true").lower() == "true"


def get_template_context():
    """Get template context with mock data if in mock mode."""
    if MOCK_MODE:
        return {
            "site_config": get_site_config(),
            "gallery_items": get_gallery_items(),
            "contact_info": get_contact_info()
        }
    return {}


@app.route("/")
def index():
    context = get_template_context()
    return render_template("index.html", **context)


@app.route("/contact")
def contact():
    context = get_template_context()
    return render_template("contact.html", **context)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
