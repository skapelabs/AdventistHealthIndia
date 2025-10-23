#!/usr/bin/env python3

import os
import re

def convert_template_to_static(template_file, output_file):
    """Convert Flask template to static HTML"""
    
    # Read the template file
    with open(template_file, 'r') as f:
        content = f.read()
    
    # Extract the content between {% block content %} and {% endblock %}
    content_match = re.search(r'{% block content %}(.*?){% endblock %}', content, re.DOTALL)
    if content_match:
        page_content = content_match.group(1).strip()
    else:
        page_content = content
    
    # Extract title from {% block title %}
    title_match = re.search(r'{% block title %}(.*?){% endblock %}', content)
    if title_match:
        page_title = title_match.group(1).strip()
    else:
        page_title = "Adventist Health India"
    
    # Create the base HTML structure
    base_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- CSS -->
    <link rel="stylesheet" href="css/style.css">
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-logo">
                <a href="/" aria-label="Adventist Health India">
                    <img src="images/logo.png" alt="Adventist Health India" class="nav-logo-img">
                </a>
            </div>
            <div class="nav-menu" id="nav-menu">
                <a href="/" class="nav-link">Home</a>
                <a href="about.html" class="nav-link">About Us</a>
                <a href="hospitals.html" class="nav-link">Hospitals</a>
                <a href="directory.html" class="nav-link">Directory</a>
                <a href="register.html" class="nav-link nav-cta">Join Us</a>
            </div>
            <div class="nav-toggle" id="nav-toggle">
                <span class="bar"></span>
                <span class="bar"></span>
                <span class="bar"></span>
            </div>
        </div>
    </nav>

{page_content}

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>Adventist Health India</h3>
                    <p>Providing compassionate healthcare services across India with excellence and faith.</p>
                </div>
                <div class="footer-section">
                    <h4>Quick Links</h4>
                    <ul>
                        <li><a href="about.html">About Us</a></li>
                        <li><a href="hospitals.html">Our Hospitals</a></li>
                        <li><a href="directory.html">Directory</a></li>
                        <li><a href="register.html">Join Us</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h4>Contact</h4>
                    <p>Email: info@adventisthealthindia.org</p>
                    <p>Phone: +91-XXX-XXXX-XXXX</p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 Adventist Health India. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <!-- JavaScript -->
    <script src="js/main.js"></script>
</body>
</html>'''
    
    # Replace Flask template variables
    base_html = base_html.replace('{{ url_for(\'home\') }}', '/')
    base_html = base_html.replace('{{ url_for(\'about\') }}', 'about.html')
    base_html = base_html.replace('{{ url_for(\'hospitals\') }}', 'hospitals.html')
    base_html = base_html.replace('{{ url_for(\'directory\') }}', 'directory.html')
    base_html = base_html.replace('{{ url_for(\'register\') }}', 'register.html')
    
    # Write the converted file
    with open(output_file, 'w') as f:
        f.write(base_html)
    
    print(f"Converted {template_file} -> {output_file}")

def main():
    """Convert all template files"""
    templates = [
        'hospitals.html',
        'directory.html', 
        'register.html',
        'admin.html',
        'hospital_detail.html'
    ]
    
    for template in templates:
        if os.path.exists(template):
            convert_template_to_static(template, template)
            print(f"✅ Converted {template}")
        else:
            print(f"❌ Template {template} not found")

if __name__ == "__main__":
    main()
