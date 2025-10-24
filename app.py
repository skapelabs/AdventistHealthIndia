from flask import Flask, render_template

app = Flask(__name__)

# Routes
@app.route('/')
def home():
    # Sample hospitals data for display
    hospitals = [
        {"id": 1, "name": "Aizawl Adventist Hospital", "city": "Aizawl", "state": "Mizoram"},
        {"id": 2, "name": "SDA Medical Centre", "city": "Bangalore", "state": "Karnataka"},
        {"id": 3, "name": "Mattison Memorial Hospital", "city": "Hapur", "state": "Uttar Pradesh"},
        {"id": 4, "name": "Pune Adventist Hospital", "city": "Pune", "state": "Maharashtra"},
        {"id": 5, "name": "Ruby Nelson Memorial Hospital", "city": "Jalandhar", "state": "Punjab"},
        {"id": 6, "name": "SDA Hospital", "city": "Ottapalam", "state": "Kerala"},
        {"id": 7, "name": "Simla Sanitarium & Hospital", "city": "Simla", "state": "Himachal Pradesh"},
        {"id": 8, "name": "SDA Hospital", "city": "Thanjavur", "state": "Tamil Nadu"},
        {"id": 9, "name": "Adventist Mission Hospital", "city": "Jengjal", "state": "Meghalaya"},
        {"id": 10, "name": "GATE Adventist Mission Hospital", "city": "Falakata", "state": "West Bengal"},
        {"id": 11, "name": "SDA College of Nursing", "city": "Ottapalam", "state": "Kerala"},
        {"id": 12, "name": "Future Facility", "city": "TBD", "state": "TBD"}
    ]
    return render_template('index.html', hospitals=hospitals)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/hospitals')
def hospitals():
    # Sample hospitals data for display
    hospitals = [
        {"id": 1, "name": "Aizawl Adventist Hospital", "city": "Aizawl", "state": "Mizoram", "address": "Aizawl, Mizoram", "phone": "+91-XXX-XXXXXXX", "email": "info@aizawlhospital.com"},
        {"id": 2, "name": "SDA Medical Centre", "city": "Bangalore", "state": "Karnataka", "address": "Bangalore, Karnataka", "phone": "+91-XXX-XXXXXXX", "email": "info@sdamedical.com"},
        {"id": 3, "name": "Mattison Memorial Hospital", "city": "Hapur", "state": "Uttar Pradesh", "address": "Hapur, Uttar Pradesh", "phone": "+91-XXX-XXXXXXX", "email": "info@mattisonhospital.com"},
        {"id": 4, "name": "Pune Adventist Hospital", "city": "Pune", "state": "Maharashtra", "address": "Pune, Maharashtra", "phone": "+91-XXX-XXXXXXX", "email": "info@puneadventist.com"},
        {"id": 5, "name": "Ruby Nelson Memorial Hospital", "city": "Jalandhar", "state": "Punjab", "address": "Jalandhar, Punjab", "phone": "+91-XXX-XXXXXXX", "email": "info@rubynelson.com"},
        {"id": 6, "name": "SDA Hospital", "city": "Ottapalam", "state": "Kerala", "address": "Ottapalam, Kerala", "phone": "+91-XXX-XXXXXXX", "email": "info@ottapalamhospital.com"},
        {"id": 7, "name": "Simla Sanitarium & Hospital", "city": "Simla", "state": "Himachal Pradesh", "address": "Simla, Himachal Pradesh", "phone": "+91-XXX-XXXXXXX", "email": "info@simlasanitarium.com"},
        {"id": 8, "name": "SDA Hospital", "city": "Thanjavur", "state": "Tamil Nadu", "address": "Thanjavur, Tamil Nadu", "phone": "+91-XXX-XXXXXXX", "email": "info@thanjavurhospital.com"},
        {"id": 9, "name": "Adventist Mission Hospital", "city": "Jengjal", "state": "Meghalaya", "address": "Jengjal, Meghalaya", "phone": "+91-XXX-XXXXXXX", "email": "info@jengjalhospital.com"},
        {"id": 10, "name": "GATE Adventist Mission Hospital", "city": "Falakata", "state": "West Bengal", "address": "Falakata, West Bengal", "phone": "+91-XXX-XXXXXXX", "email": "info@gatehospital.com"},
        {"id": 11, "name": "SDA College of Nursing", "city": "Ottapalam", "state": "Kerala", "address": "Ottapalam, Kerala", "phone": "+91-XXX-XXXXXXX", "email": "info@nursingcollege.com"},
        {"id": 12, "name": "Future Facility", "city": "TBD", "state": "TBD", "address": "To be determined", "phone": "TBD", "email": "TBD"}
    ]
    return render_template('hospitals.html', hospitals=hospitals)

@app.route('/hospitals/<int:hospital_id>')
def hospital_detail(hospital_id):
    # Sample hospital data for display
    hospitals = {
        1: {"id": 1, "name": "Aizawl Adventist Hospital", "city": "Aizawl", "state": "Mizoram", "address": "Aizawl, Mizoram", "phone": "+91-XXX-XXXXXXX", "email": "info@aizawlhospital.com", "description": "A leading healthcare facility in Mizoram providing comprehensive medical services."},
        2: {"id": 2, "name": "SDA Medical Centre", "city": "Bangalore", "state": "Karnataka", "address": "Bangalore, Karnataka", "phone": "+91-XXX-XXXXXXX", "email": "info@sdamedical.com", "description": "Modern medical center in Bangalore offering specialized healthcare services."},
        3: {"id": 3, "name": "Mattison Memorial Hospital", "city": "Hapur", "state": "Uttar Pradesh", "address": "Hapur, Uttar Pradesh", "phone": "+91-XXX-XXXXXXX", "email": "info@mattisonhospital.com", "description": "Memorial hospital dedicated to providing quality healthcare in Uttar Pradesh."},
        4: {"id": 4, "name": "Pune Adventist Hospital", "city": "Pune", "state": "Maharashtra", "address": "Pune, Maharashtra", "phone": "+91-XXX-XXXXXXX", "email": "info@puneadventist.com", "description": "Comprehensive healthcare services in the heart of Pune."},
        5: {"id": 5, "name": "Ruby Nelson Memorial Hospital", "city": "Jalandhar", "state": "Punjab", "address": "Jalandhar, Punjab", "phone": "+91-XXX-XXXXXXX", "email": "info@rubynelson.com", "description": "Memorial hospital serving the community of Jalandhar with excellence."},
        6: {"id": 6, "name": "SDA Hospital", "city": "Ottapalam", "state": "Kerala", "address": "Ottapalam, Kerala", "phone": "+91-XXX-XXXXXXX", "email": "info@ottapalamhospital.com", "description": "Healthcare facility in Kerala providing quality medical care."},
        7: {"id": 7, "name": "Simla Sanitarium & Hospital", "city": "Simla", "state": "Himachal Pradesh", "address": "Simla, Himachal Pradesh", "phone": "+91-XXX-XXXXXXX", "email": "info@simlasanitarium.com", "description": "Sanitarium and hospital in the beautiful hills of Simla."},
        8: {"id": 8, "name": "SDA Hospital", "city": "Thanjavur", "state": "Tamil Nadu", "address": "Thanjavur, Tamil Nadu", "phone": "+91-XXX-XXXXXXX", "email": "info@thanjavurhospital.com", "description": "Healthcare services in Tamil Nadu's cultural capital."},
        9: {"id": 9, "name": "Adventist Mission Hospital", "city": "Jengjal", "state": "Meghalaya", "address": "Jengjal, Meghalaya", "phone": "+91-XXX-XXXXXXX", "email": "info@jengjalhospital.com", "description": "Mission hospital serving the community of Meghalaya."},
        10: {"id": 10, "name": "GATE Adventist Mission Hospital", "city": "Falakata", "state": "West Bengal", "address": "Falakata, West Bengal", "phone": "+91-XXX-XXXXXXX", "email": "info@gatehospital.com", "description": "Mission hospital in West Bengal providing healthcare services."},
        11: {"id": 11, "name": "SDA College of Nursing", "city": "Ottapalam", "state": "Kerala", "address": "Ottapalam, Kerala", "phone": "+91-XXX-XXXXXXX", "email": "info@nursingcollege.com", "description": "Educational institution training future healthcare professionals."},
        12: {"id": 12, "name": "Future Facility", "city": "TBD", "state": "TBD", "address": "To be determined", "phone": "TBD", "email": "TBD", "description": "Future healthcare facility to be established."}
    }
    
    hospital = hospitals.get(hospital_id)
    if not hospital:
        return "Hospital not found", 404
    
    return render_template('hospital_detail.html', hospital=hospital)

@app.route('/directory')
def directory():
    # Sample professionals data for display
    professionals = [
        {"id": 1, "name": "Dr. John Smith", "designation": "Chief Medical Officer", "hospital": "Aizawl Adventist Hospital", "specialization": "Internal Medicine", "role": "Doctor"},
        {"id": 2, "name": "Dr. Sarah Johnson", "designation": "Pediatrician", "hospital": "SDA Medical Centre", "specialization": "Pediatrics", "role": "Doctor"},
        {"id": 3, "name": "Nurse Mary Wilson", "designation": "Head Nurse", "hospital": "Mattison Memorial Hospital", "specialization": "Critical Care", "role": "Nurse"},
        {"id": 4, "name": "Dr. Michael Brown", "designation": "Cardiologist", "hospital": "Pune Adventist Hospital", "specialization": "Cardiology", "role": "Doctor"},
        {"id": 5, "name": "Dr. Emily Davis", "designation": "Gynecologist", "hospital": "Ruby Nelson Memorial Hospital", "specialization": "Gynecology", "role": "Doctor"}
    ]
    
    hospitals = [
        {"id": 1, "name": "Aizawl Adventist Hospital"},
        {"id": 2, "name": "SDA Medical Centre"},
        {"id": 3, "name": "Mattison Memorial Hospital"},
        {"id": 4, "name": "Pune Adventist Hospital"},
        {"id": 5, "name": "Ruby Nelson Memorial Hospital"},
        {"id": 6, "name": "SDA Hospital"},
        {"id": 7, "name": "Simla Sanitarium & Hospital"},
        {"id": 8, "name": "SDA Hospital"},
        {"id": 9, "name": "Adventist Mission Hospital"},
        {"id": 10, "name": "GATE Adventist Mission Hospital"},
        {"id": 11, "name": "SDA College of Nursing"},
        {"id": 12, "name": "Future Facility"}
    ]
    
    return render_template('directory.html', professionals=professionals, hospitals=hospitals)

@app.route('/register')
def register():
    # Sample hospitals data for the form
    hospitals = [
        {"id": 1, "name": "Aizawl Adventist Hospital"},
        {"id": 2, "name": "SDA Medical Centre"},
        {"id": 3, "name": "Mattison Memorial Hospital"},
        {"id": 4, "name": "Pune Adventist Hospital"},
        {"id": 5, "name": "Ruby Nelson Memorial Hospital"},
        {"id": 6, "name": "SDA Hospital"},
        {"id": 7, "name": "Simla Sanitarium & Hospital"},
        {"id": 8, "name": "SDA Hospital"},
        {"id": 9, "name": "Adventist Mission Hospital"},
        {"id": 10, "name": "GATE Adventist Mission Hospital"},
        {"id": 11, "name": "SDA College of Nursing"},
        {"id": 12, "name": "Future Facility"}
    ]
    return render_template('register.html', hospitals=hospitals)

if __name__ == '__main__':
    app.run(debug=True, port=5000)