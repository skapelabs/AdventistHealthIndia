from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
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
    description = db.Column(db.Text)
    banner_image = db.Column(db.String(200))
    medical_director_name = db.Column(db.String(200))
    medical_director_bio = db.Column(db.Text)
    medical_director_photo = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Professional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    specialization = db.Column(db.String(200))
    bio = db.Column(db.Text)
    profile_photo = db.Column(db.String(200))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    role = db.Column(db.String(50), nullable=False)  # Doctor, Nurse, Technician, etc.
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    hospital = db.relationship('Hospital', backref=db.backref('professionals', lazy=True))

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def home():
    hospitals = Hospital.query.limit(12).all()
    return render_template('index.html', hospitals=hospitals)

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
    hospital_filter = request.args.get('hospital')
    specialization_filter = request.args.get('specialization')
    role_filter = request.args.get('role')
    
    query = Professional.query.filter_by(is_approved=True)
    
    if hospital_filter:
        query = query.filter_by(hospital_id=hospital_filter)
    if specialization_filter:
        query = query.filter(Professional.specialization.contains(specialization_filter))
    if role_filter:
        query = query.filter_by(role=role_filter)
    
    professionals = query.all()
    hospitals = Hospital.query.all()
    
    return render_template('directory.html', professionals=professionals, hospitals=hospitals)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        designation = request.form['designation']
        hospital_id = request.form['hospital_id']
        specialization = request.form['specialization']
        bio = request.form['bio']
        email = request.form['email']
        phone = request.form['phone']
        role = request.form['role']
        
        professional = Professional(
            name=name,
            designation=designation,
            hospital_id=hospital_id,
            specialization=specialization,
            bio=bio,
            email=email,
            phone=phone,
            role=role
        )
        
        db.session.add(professional)
        db.session.commit()
        
        flash('Registration submitted successfully! Your profile will be reviewed and approved by our admin team.')
        return redirect(url_for('directory'))
    
    hospitals = Hospital.query.all()
    return render_template('register.html', hospitals=hospitals)

@app.route('/admin')
def admin():
    pending_professionals = Professional.query.filter_by(is_approved=False).all()
    hospitals = Hospital.query.all()
    return render_template('admin.html', pending_professionals=pending_professionals, hospitals=hospitals)

@app.route('/admin/approve/<int:professional_id>')
def approve_professional(professional_id):
    professional = Professional.query.get_or_404(professional_id)
    professional.is_approved = True
    db.session.commit()
    flash(f'Professional {professional.name} has been approved!')
    return redirect(url_for('admin'))

@app.route('/admin/reject/<int:professional_id>')
def reject_professional(professional_id):
    professional = Professional.query.get_or_404(professional_id)
    db.session.delete(professional)
    db.session.commit()
    flash(f'Professional {professional.name} has been rejected and removed.')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Add sample hospitals if they don't exist
        if Hospital.query.count() == 0:
            sample_hospitals = [
                Hospital(name="Aizawl Adventist Hospital", state="Mizoram", city="Aizawl"),
                Hospital(name="SDA Medical Centre", state="Karnataka", city="Bangalore"),
                Hospital(name="Mattison Memorial Hospital", state="Uttar Pradesh", city="Hapur"),
                Hospital(name="Pune Adventist Hospital", state="Maharashtra", city="Pune"),
                Hospital(name="Ruby Nelson Memorial Hospital", state="Punjab", city="Jalandhar"),
                Hospital(name="SDA Hospital", state="Kerala", city="Ottapalam"),
                Hospital(name="Simla Sanitarium & Hospital", state="Himachal Pradesh", city="Simla"),
                Hospital(name="SDA Hospital", state="Tamil Nadu", city="Thanjavur"),
                Hospital(name="Adventist Mission Hospital", state="Meghalaya", city="Jengjal"),
                Hospital(name="GATE Adventist Mission Hospital", state="West Bengal", city="Falakata"),
                Hospital(name="SDA College of Nursing", state="Kerala", city="Ottapalam"),
                Hospital(name="Future Facility", state="TBD", city="TBD")
            ]
            
            for hospital in sample_hospitals:
                db.session.add(hospital)
            
            db.session.commit()
    
    app.run(debug=True, port=6990)
