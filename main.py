#!/usr/bin/env python3
"""
Web Medical Management System
Run with: python main.py
"""
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import sqlite3
import os
from datetime import datetime
from fpdf import FPDF
import io

app = Flask(__name__)
app.secret_key = 'medical-system-secret-key-2024'
DATABASE = 'data/medical.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database from schema.sql"""
    if not os.path.exists('data'):
        os.makedirs('data')
    
    conn = get_db()
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

def add_sample_data():
    """Add sample data for demonstration and evaluation"""
    conn = get_db()
    
    # Check if data already exists
    patient_count = conn.execute('SELECT COUNT(*) as count FROM Patients').fetchone()['count']
    if patient_count > 0:
        conn.close()
        return  # Data already exists
    
    # Add sample patients
    sample_patients = [
        ('John', 'Doe', '1980-05-15', 'Male', '555-0101'),
        ('Jane', 'Smith', '1992-08-22', 'Female', '555-0102'),
        ('Robert', 'Johnson', '1975-12-10', 'Male', '555-0103'),
        ('Emily', 'Davis', '1988-03-25', 'Female', '555-0104'),
        ('Michael', 'Brown', '1995-07-08', 'Male', '555-0105'),
    ]
    
    for first, last, dob, gender, contact in sample_patients:
        conn.execute('''
            INSERT INTO Patients (first_name, last_name, dob, gender, contact)
            VALUES (?, ?, ?, ?, ?)
        ''', (first, last, dob, gender, contact))
    
    # Get patient IDs for appointments and diagnostics
    patients = conn.execute('SELECT id FROM Patients').fetchall()
    
    # Add sample appointments
    if patients:
        conn.execute('''
            INSERT INTO Appointments (patient_id, appt_datetime, reason, status)
            VALUES (?, ?, ?, ?)
        ''', (patients[0]['id'], '2024-12-15 10:00', 'Regular checkup', 'scheduled'))
        
        conn.execute('''
            INSERT INTO Appointments (patient_id, appt_datetime, reason, status)
            VALUES (?, ?, ?, ?)
        ''', (patients[1]['id'], '2024-12-10 14:30', 'Follow-up appointment', 'completed'))
        
        conn.execute('''
            INSERT INTO Appointments (patient_id, appt_datetime, reason, status)
            VALUES (?, ?, ?, ?)
        ''', (patients[2]['id'], '2024-12-20 09:00', 'Consultation', 'scheduled'))
    
    # Add sample diagnostics
    if patients:
        conn.execute('''
            INSERT INTO Diagnostics (patient_id, diag_datetime, notes)
            VALUES (?, ?, ?)
        ''', (patients[0]['id'], '2024-11-01 10:00', 'Blood pressure: 120/80. Heart rate: 72 bpm. All vitals normal.'))
        
        conn.execute('''
            INSERT INTO Diagnostics (patient_id, diag_datetime, notes)
            VALUES (?, ?, ?)
        ''', (patients[1]['id'], '2024-11-05 14:00', 'Blood test results: Hemoglobin 14.2 g/dL, Glucose 95 mg/dL. All values within normal range.'))
        
        conn.execute('''
            INSERT INTO Diagnostics (patient_id, diag_datetime, notes)
            VALUES (?, ?, ?)
        ''', (patients[0]['id'], '2024-11-10 11:00', 'X-Ray examination: No abnormalities detected. Chest clear.'))
    
    conn.commit()
    conn.close()

# Initialize database on startup
if not os.path.exists(DATABASE):
    init_db()
    # Add sample data for demonstration
    add_sample_data()

# Dashboard - Home page
@app.route('/')
def dashboard():
    conn = get_db()
    
    # Get counts
    total_patients = conn.execute('SELECT COUNT(*) as count FROM Patients').fetchone()['count']
    total_appointments = conn.execute('SELECT COUNT(*) as count FROM Appointments').fetchone()['count']
    total_diagnostics = conn.execute('SELECT COUNT(*) as count FROM Diagnostics').fetchone()['count']
    
    # Get appointments by status for chart
    appointments_by_status = conn.execute('''
        SELECT status, COUNT(*) as count 
        FROM Appointments 
        GROUP BY status
    ''').fetchall()
    
    # Get patients by gender for chart
    patients_by_gender = conn.execute('''
        SELECT gender, COUNT(*) as count 
        FROM Patients 
        WHERE gender IS NOT NULL
        GROUP BY gender
    ''').fetchall()
    
    conn.close()
    
    return render_template('dashboard.html',
                         total_patients=total_patients,
                         total_appointments=total_appointments,
                         total_diagnostics=total_diagnostics,
                         appointments_by_status=appointments_by_status,
                         patients_by_gender=patients_by_gender)

# Patient routes
@app.route('/patients')
def patient_list():
    conn = get_db()
    patients = conn.execute('SELECT * FROM Patients ORDER BY last_name, first_name').fetchall()
    conn.close()
    return render_template('patient_list.html', patients=patients)

@app.route('/patients/new', methods=['GET', 'POST'])
def patient_new():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form.get('dob', '')
        gender = request.form.get('gender', '')
        contact = request.form.get('contact', '')
        
        conn = get_db()
        conn.execute('''
            INSERT INTO Patients (first_name, last_name, dob, gender, contact)
            VALUES (?, ?, ?, ?, ?)
        ''', (first_name, last_name, dob, gender, contact))
        conn.commit()
        conn.close()
        
        flash('Patient added successfully!', 'success')
        return redirect(url_for('patient_list'))
    
    return render_template('patient_form.html')

@app.route('/patients/<int:id>/edit', methods=['GET', 'POST'])
def patient_edit(id):
    conn = get_db()
    patient = conn.execute('SELECT * FROM Patients WHERE id = ?', (id,)).fetchone()
    
    if not patient:
        flash('Patient not found!', 'error')
        conn.close()
        return redirect(url_for('patient_list'))
    
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form.get('dob', '')
        gender = request.form.get('gender', '')
        contact = request.form.get('contact', '')
        
        conn.execute('''
            UPDATE Patients 
            SET first_name = ?, last_name = ?, dob = ?, gender = ?, contact = ?
            WHERE id = ?
        ''', (first_name, last_name, dob, gender, contact, id))
        conn.commit()
        conn.close()
        
        flash('Patient updated successfully!', 'success')
        return redirect(url_for('patient_view', id=id))
    
    conn.close()
    return render_template('patient_form.html', patient=patient)

@app.route('/patients/<int:id>')
def patient_view(id):
    conn = get_db()
    patient = conn.execute('SELECT * FROM Patients WHERE id = ?', (id,)).fetchone()
    
    if not patient:
        flash('Patient not found!', 'error')
        return redirect(url_for('patient_list'))
    
    appointments = conn.execute('''
        SELECT * FROM Appointments 
        WHERE patient_id = ? 
        ORDER BY appt_datetime DESC
    ''', (id,)).fetchall()
    
    diagnostics = conn.execute('''
        SELECT * FROM Diagnostics 
        WHERE patient_id = ? 
        ORDER BY diag_datetime DESC
    ''', (id,)).fetchall()
    
    conn.close()
    return render_template('patient_view.html', patient=patient, appointments=appointments, diagnostics=diagnostics)

@app.route('/patients/<int:id>/delete', methods=['POST'])
def patient_delete(id):
    conn = get_db()
    conn.execute('DELETE FROM Patients WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Patient deleted successfully!', 'success')
    return redirect(url_for('patient_list'))

# Appointment routes
@app.route('/appointments')
def appointment_list():
    conn = get_db()
    appointments = conn.execute('''
        SELECT a.*, p.first_name, p.last_name 
        FROM Appointments a
        LEFT JOIN Patients p ON a.patient_id = p.id
        ORDER BY a.appt_datetime DESC
    ''').fetchall()
    conn.close()
    return render_template('appointment_list.html', appointments=appointments)

@app.route('/appointments/new', methods=['GET', 'POST'])
def appointment_new():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        appt_datetime = request.form['appt_datetime']
        reason = request.form.get('reason', '')
        status = request.form.get('status', 'scheduled')
        
        conn = get_db()
        conn.execute('''
            INSERT INTO Appointments (patient_id, appt_datetime, reason, status)
            VALUES (?, ?, ?, ?)
        ''', (patient_id, appt_datetime, reason, status))
        conn.commit()
        conn.close()
        
        flash('Appointment scheduled successfully!', 'success')
        return redirect(url_for('appointment_list'))
    
    conn = get_db()
    patients = conn.execute('SELECT * FROM Patients ORDER BY last_name, first_name').fetchall()
    conn.close()
    return render_template('appointment_form.html', patients=patients)

@app.route('/appointments/<int:id>/edit', methods=['GET', 'POST'])
def appointment_edit(id):
    conn = get_db()
    appointment = conn.execute('SELECT * FROM Appointments WHERE id = ?', (id,)).fetchone()
    
    if not appointment:
        flash('Appointment not found!', 'error')
        conn.close()
        return redirect(url_for('appointment_list'))
    
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        appt_datetime = request.form['appt_datetime']
        reason = request.form.get('reason', '')
        status = request.form.get('status', 'scheduled')
        
        conn.execute('''
            UPDATE Appointments 
            SET patient_id = ?, appt_datetime = ?, reason = ?, status = ?
            WHERE id = ?
        ''', (patient_id, appt_datetime, reason, status, id))
        conn.commit()
        conn.close()
        
        flash('Appointment updated successfully!', 'success')
        return redirect(url_for('appointment_list'))
    
    patients = conn.execute('SELECT * FROM Patients ORDER BY last_name, first_name').fetchall()
    conn.close()
    return render_template('appointment_form.html', patients=patients, appointment=appointment)

@app.route('/appointments/<int:id>/delete', methods=['POST'])
def appointment_delete(id):
    conn = get_db()
    conn.execute('DELETE FROM Appointments WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Appointment deleted successfully!', 'success')
    return redirect(url_for('appointment_list'))

@app.route('/appointments/<int:id>/complete', methods=['POST'])
def appointment_complete(id):
    conn = get_db()
    conn.execute('UPDATE Appointments SET status = ? WHERE id = ?', ('completed', id))
    conn.commit()
    conn.close()
    flash('Appointment marked as completed!', 'success')
    return redirect(url_for('appointment_list'))

# Diagnostics routes
@app.route('/diagnostics/<int:patient_id>', methods=['GET', 'POST'])
def diagnostics(patient_id):
    conn = get_db()
    patient = conn.execute('SELECT * FROM Patients WHERE id = ?', (patient_id,)).fetchone()
    
    if not patient:
        flash('Patient not found!', 'error')
        return redirect(url_for('patient_list'))
    
    if request.method == 'POST':
        diag_datetime = request.form['diag_datetime']
        notes = request.form.get('notes', '')
        
        conn.execute('''
            INSERT INTO Diagnostics (patient_id, diag_datetime, notes)
            VALUES (?, ?, ?)
        ''', (patient_id, diag_datetime, notes))
        conn.commit()
        flash('Diagnostic record added successfully!', 'success')
    
    diagnostics_list = conn.execute('''
        SELECT * FROM Diagnostics 
        WHERE patient_id = ? 
        ORDER BY diag_datetime DESC
    ''', (patient_id,)).fetchall()
    
    conn.close()
    return render_template('diagnostics.html', patient=patient, diagnostics=diagnostics_list)

# PDF Export
@app.route('/export/patient/<int:id>')
def export_patient(id):
    conn = get_db()
    patient = conn.execute('SELECT * FROM Patients WHERE id = ?', (id,)).fetchone()
    
    if not patient:
        flash('Patient not found!', 'error')
        return redirect(url_for('patient_list'))
    
    appointments = conn.execute('''
        SELECT * FROM Appointments 
        WHERE patient_id = ? 
        ORDER BY appt_datetime DESC
    ''', (id,)).fetchall()
    
    diagnostics = conn.execute('''
        SELECT * FROM Diagnostics 
        WHERE patient_id = ? 
        ORDER BY diag_datetime DESC
    ''', (id,)).fetchall()
    
    conn.close()
    
    # Generate PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Header
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Patient Medical Report', 0, 1, 'C')
    pdf.ln(10)
    
    # Patient Details
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Patient Information', 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 6, f"Name: {patient['first_name']} {patient['last_name']}", 0, 1)
    if patient['dob']:
        pdf.cell(0, 6, f"Date of Birth: {patient['dob']}", 0, 1)
    if patient['gender']:
        pdf.cell(0, 6, f"Gender: {patient['gender']}", 0, 1)
    if patient['contact']:
        pdf.cell(0, 6, f"Contact: {patient['contact']}", 0, 1)
    pdf.ln(5)
    
    # Appointments
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Appointments', 0, 1)
    pdf.set_font('Arial', '', 9)
    if appointments:
        for apt in appointments:
            pdf.cell(0, 6, f"Date: {apt['appt_datetime']} | Status: {apt['status']}", 0, 1)
            if apt['reason']:
                pdf.cell(0, 6, f"Reason: {apt['reason']}", 0, 1)
            pdf.ln(2)
    else:
        pdf.cell(0, 6, 'No appointments recorded.', 0, 1)
    pdf.ln(5)
    
    # Diagnostics
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Diagnostics', 0, 1)
    pdf.set_font('Arial', '', 9)
    if diagnostics:
        for diag in diagnostics:
            pdf.cell(0, 6, f"Date: {diag['diag_datetime']}", 0, 1)
            if diag['notes']:
                pdf.multi_cell(0, 6, f"Notes: {diag['notes']}")
            pdf.ln(2)
    else:
        pdf.cell(0, 6, 'No diagnostics recorded.', 0, 1)
    
    # Footer
    pdf.set_y(-15)
    pdf.set_font('Arial', 'I', 8)
    pdf.cell(0, 10, f'Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 0, 'C')
    
    # Save to bytes
    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    
    return send_file(pdf_output, mimetype='application/pdf', 
                    as_attachment=True, 
                    download_name=f'patient_{id}_report.pdf')

if __name__ == '__main__':
    print("=" * 60)
    print("Medical Management System")
    print("=" * 60)
    print("Starting server...")
    print("Open your browser and go to: http://localhost:5000")
    print("Press CTRL+C to stop the server")
    print("=" * 60)
    app.run(host='127.0.0.1', port=5000, debug=True)


