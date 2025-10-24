# Adventist Health India

A simple Flask web application for Adventist Health India showcasing their hospital network and healthcare professionals.

## Features

- **Home Page**: Overview of the organization and hospital network
- **About Page**: Information about Adventist Health India
- **Hospitals Page**: List of all 12 hospitals across India
- **Hospital Details**: Individual hospital information
- **Directory Page**: Healthcare professionals directory
- **Registration Page**: Professional registration form (display only)

## Project Structure

```
├── app.py                 # Flask application
├── requirements.txt      # Python dependencies
├── static/               # Static assets
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   ├── images/
│   │   └── logo.png      # Organization logo
│   └── js/
│       └── main.js       # JavaScript functionality
└── templates/            # HTML templates
    ├── base.html         # Base template
    ├── index.html        # Home page
    ├── about.html        # About page
    ├── hospitals.html    # Hospitals listing
    ├── hospital_detail.html # Individual hospital
    ├── directory.html    # Professionals directory
    └── register.html     # Registration form
```

## Installation

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. Open your browser and visit `http://localhost:5000`

## Technologies Used

- **Flask**: Python web framework
- **HTML/CSS/JavaScript**: Frontend technologies
- **Responsive Design**: Mobile-friendly interface

## Notes

This is a simplified version of the original complex application. All database functionality, API integrations, and complex features have been removed to maintain a basic, clean structure with just HTML, CSS, JavaScript, and Flask routing.

