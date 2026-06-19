import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from google import genai
from google.genai import types

app = Flask(__name__)
app.secret_key = "health_app_secret_key"
DATABASE = "database.db"

# Initialize Google GenAI Client
# It automatically picks up the GEMINI_API_KEY environment variable
try:
    ai_client = genai.Client()
except Exception as e:
    print(f"Warning: AI Client failed to initialize. Check GEMINI_API_KEY. Error: {e}")
    ai_client = None

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                dob TEXT NOT NULL,
                email TEXT NOT NULL,
                glucose REAL NOT NULL,
                haemoglobin REAL NOT NULL,
                cholesterol REAL NOT NULL,
                remarks TEXT
            )
        ''')
        conn.commit()

# --- AI Integration Layer ---
def generate_health_remarks(glucose, haemoglobin, cholesterol):
    """Calls Gemini 2.5 Flash to generate a health prediction/risk analysis."""
    if not ai_client:
        return "AI Analysis Unavailable: API Key not configured properly."
    
    prompt = f"""
    You are an expert medical AI assistant. Analyze these patient blood test metrics:
    - Glucose: {glucose} mg/dL
    - Haemoglobin: {haemoglobin} g/dL
    - Total Cholesterol: {cholesterol} mg/dL
    
    Provide a concise, 2-sentence health risk summary and actionable dietary advice. 
    Keep it professional, empathetic, and clear. Do not use markdown formatting.
    """
    
    try:
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3, # Low temperature for more deterministic, factual output
            )
        )
        return response.text.strip()
    except Exception as e:
        return f"Prediction Error: Unable to fetch AI remarks at this time. ({str(e)})"

# --- Server-Side Validation ---
def validate_patient_data(data):
    errors = []
    
    # 1. Date of Birth Validation
    try:
        dob_date = datetime.strptime(data['dob'], '%Y-%m-%d').date()
        if dob_date > datetime.today().date():
            errors.append("Date of Birth cannot be in the future.")
    except ValueError:
        errors.append("Invalid Date of Birth format.")
        
    # 2. Blood test values numeric check
    for field in ['glucose', 'haemoglobin', 'cholesterol']:
        try:
            val = float(data[field])
            if val < 0:
                errors.append(f"{field.capitalize()} must be a positive number.")
        except ValueError:
            errors.append(f"{field.capitalize()} must be a valid number.")
            
    return errors

# --- Routes (CRUD) ---

@app.route('/')
def index():
    conn = get_db_connection()
    patients = conn.execute('SELECT * FROM patients ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', patients=patients)

@app.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
        patient_data = {
            'full_name': request.form['full_name'].strip(),
            'dob': request.form['dob'],
            'email': request.form['email'].strip(),
            'glucose': request.form['glucose'],
            'haemoglobin': request.form['haemoglobin'],
            'cholesterol': request.form['cholesterol']
        }
        
        errors = validate_patient_data(patient_data)
        if errors:
            for error in errors:
                flash(error, "error")
            return redirect(url_for('index'))
        
        # Trigger AI analysis using validated data
        remarks = generate_health_remarks(
            patient_data['glucose'], 
            patient_data['haemoglobin'], 
            patient_data['cholesterol']
        )
        
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO patients (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (patient_data['full_name'], patient_data['dob'], patient_data['email'], 
              patient_data['glucose'], patient_data['haemoglobin'], patient_data['cholesterol'], remarks))
        conn.commit()
        conn.close()
        
        flash("Patient profile successfully created and analyzed!", "success")
        return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    patient_data = {
        'full_name': request.form['full_name'].strip(),
        'dob': request.form['dob'],
        'email': request.form['email'].strip(),
        'glucose': request.form['glucose'],
        'haemoglobin': request.form['haemoglobin'],
        'cholesterol': request.form['cholesterol']
    }
    
    errors = validate_patient_data(patient_data)
    if errors:
        for error in errors:
            flash(error, "error")
        return redirect(url_for('index'))
    
    # Re-trigger AI insights based on updated blood metrics
    remarks = generate_health_remarks(
        patient_data['glucose'], 
        patient_data['haemoglobin'], 
        patient_data['cholesterol']
    )
    
    conn = get_db_connection()
    conn.execute('''
        UPDATE patients 
        SET full_name=?, dob=?, email=?, glucose=?, haemoglobin=?, cholesterol=?, remarks=?
        WHERE id=?
    ''', (patient_data['full_name'], patient_data['dob'], patient_data['email'], 
          patient_data['glucose'], patient_data['haemoglobin'], patient_data['cholesterol'], remarks, id))
    conn.commit()
    conn.close()
    
    flash("Patient profile successfully updated!", "success")
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM patients WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash("Patient record deleted.", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
