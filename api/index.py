from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import json

# Create Flask app
app = Flask(__name__, 
           template_folder='../../templates',
           static_folder='../../static')
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adventist_health.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    website = db.Column(db.String(200))
    description = db.Column(db.Text)
    services = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Professional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    hospital = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100))
    bio = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Routes
@app.route('/')
def home():
    # Get some sample data for the homepage
    hospitals = Hospital.query.limit(12).all()
    professionals = Professional.query.filter_by(status='approved').limit(6).all()
    
    return render_template('index.html', 
                         hospitals=hospitals, 
                         professionals=professionals)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/hospitals')
def hospitals():
    hospitals = Hospital.query.all()
    return render_template('hospitals.html', hospitals=hospitals)

@app.route('/hospitals/<int:hospital_id>')
def hospital_detail(hospital_id):
    hospital = Hospital.query.get_or_404(hospital_id)
    return render_template('hospital_detail.html', hospital=hospital)

@app.route('/directory')
def directory():
    professionals = Professional.query.filter_by(status='approved').all()
    return render_template('directory.html', professionals=professionals)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle registration form
        name = request.form.get('name')
        email = request.form.get('email')
        hospital = request.form.get('hospital')
        role = request.form.get('role')
        specialty = request.form.get('specialty')
        bio = request.form.get('bio')
        
        # Check if email already exists
        existing_professional = Professional.query.filter_by(email=email).first()
        if existing_professional:
            flash('This email is already registered.', 'error')
            return redirect(url_for('register'))
        
        # Create new professional
        professional = Professional(
            name=name,
            email=email,
            hospital=hospital,
            role=role,
            specialty=specialty,
            bio=bio,
            status='pending'
        )
        
        db.session.add(professional)
        db.session.commit()
        
        flash('Registration submitted successfully! You will be notified once approved.', 'success')
        return redirect(url_for('directory'))
    
    return render_template('register.html')

@app.route('/admin')
def admin():
    professionals = Professional.query.filter_by(status='pending').all()
    return render_template('admin.html', professionals=professionals)

@app.route('/admin/approve/<int:professional_id>')
def approve_professional(professional_id):
    professional = Professional.query.get_or_404(professional_id)
    professional.status = 'approved'
    professional.updated_at = datetime.utcnow()
    db.session.commit()
    
    flash(f'{professional.name} has been approved.', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/reject/<int:professional_id>')
def reject_professional(professional_id):
    professional = Professional.query.get_or_404(professional_id)
    professional.status = 'rejected'
    professional.updated_at = datetime.utcnow()
    db.session.commit()
    
    flash(f'{professional.name} has been rejected.', 'success')
    return redirect(url_for('admin'))

# Vercel serverless function handler
def handler(request):
    return app(request.environ, lambda *args: None)
