#!/usr/bin/env python3
"""
Static site generator for frontend preview.

This script generates a static version of the site using mock data,
which can be deployed as a preview for pull requests.
"""

import os
import shutil
from pathlib import Path

from flask import Flask
from jinja2 import Environment, FileSystemLoader

from mock_data import get_gallery_items, get_site_config, get_contact_info


def generate_static_site(output_dir: str = "_preview"):
    """Generate a static version of the site for preview."""
    
    # Setup paths
    base_dir = Path(__file__).parent
    output_path = base_dir / output_dir
    templates_dir = base_dir / "templates"
    static_dir = base_dir / "static"
    
    # Clean and create output directory
    if output_path.exists():
        shutil.rmtree(output_path)
    output_path.mkdir(parents=True)
    
    # Copy static files
    if static_dir.exists():
        shutil.copytree(static_dir, output_path / "static")
    
    # Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader(str(templates_dir)))
    
    # Get mock data
    site_config = get_site_config()
    gallery_items = get_gallery_items()
    contact_info = get_contact_info()
    
    # Define url_for replacement for static site
    def url_for(endpoint, **kwargs):
        if endpoint == 'static':
            filename = kwargs.get('filename', '')
            return f"./static/{filename}"
        elif endpoint == 'index':
            return "./index.html"
        elif endpoint == 'contact':
            return "./contact.html"
        return "#"
    
    # Add url_for to template globals
    env.globals['url_for'] = url_for
    
    # Generate index.html
    index_template = env.get_template("index.html")
    index_html = index_template.render(
        site_config=site_config,
        gallery_items=gallery_items
    )
    (output_path / "index.html").write_text(index_html)
    print(f"Generated: {output_path / 'index.html'}")
    
    # Generate contact.html
    contact_template = env.get_template("contact.html")
    contact_html = contact_template.render(
        site_config=site_config,
        contact_info=contact_info
    )
    (output_path / "contact.html").write_text(contact_html)
    print(f"Generated: {output_path / 'contact.html'}")
    
    print(f"\nStatic site generated in: {output_path}")
    print(f"To preview, open: {output_path / 'index.html'}")
    
    return str(output_path)


if __name__ == "__main__":
    generate_static_site()
