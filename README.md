# Web Medical Management System

A simple, local Flask-based web application for managing patients, appointments, and diagnostic records.

## Quick Start

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

Or if using virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python main.py
```

The server will start on **http://localhost:5000**

### Step 3: Open in Browser
Navigate to **http://localhost:5000** in your web browser.

## Pre-loaded Sample Data

The application comes with **sample data** for easy evaluation:

- ✅ **5 Sample Patients**: John Doe, Jane Smith, Robert Johnson, Emily Davis, Michael Brown
- ✅ **3 Sample Appointments**: Mix of scheduled and completed appointments
- ✅ **3 Sample Diagnostic Records**: Various test results and medical notes

**Note**: Sample data is automatically loaded on first run. To reset, delete `data/medical.db` and restart the application.

## Features

- **Patient Management**: Add, view, edit, and delete patient records
- **Appointment Scheduling**: Schedule, view, edit, and manage appointments linked to patients
- **Diagnostics**: Record diagnostic notes for each patient
- **Dashboard**: View statistics and interactive charts (Chart.js)
- **PDF Export**: Generate comprehensive PDF reports for patients (FPDF)

## Technology Stack

- **Backend**: Python Flask framework
- **Database**: SQLite (local, no server required)
- **Frontend**: Bootstrap 5.3.0 (responsive design)
- **Charts**: Chart.js 4.4.0 (data visualization)
- **PDF**: FPDF2 library (report generation)

## Usage Guide

### Dashboard (Home Page)
- View summary statistics: Total Patients, Appointments, Diagnostics
- Interactive charts: Appointments by Status (bar chart), Patients by Gender (pie chart)
- All charts are generated using Chart.js library

### Patient Management
- **View Patients**: Click "Patients" in navigation to see all registered patients
- **Add Patient**: Click "Add New Patient" button, fill in details (First Name, Last Name, DOB, Gender, Contact)
- **Edit Patient**: Click "Edit" button next to any patient to modify their information
- **View Patient Details**: Click "View" to see complete patient information including appointment history and diagnostics
- **Delete Patient**: Click "Delete" button (removes patient and all associated records)
- **Export PDF**: Click "Export PDF" to generate comprehensive patient report

### Appointment Management
- **View Appointments**: Click "Appointments" in navigation to see all scheduled appointments
- **Schedule Appointment**: Click "Schedule New Appointment", select patient, set date/time, reason, and status
- **Edit Appointment**: Click "Edit" button to modify appointment details
- **Mark Complete**: Click "Mark Complete" to change appointment status to completed
- **Delete Appointment**: Click "Delete" button to remove appointment

### Diagnostic Records
- **View Diagnostics**: Click "Diagnostics" button from patient list or patient view
- **Add Diagnostic**: Fill in date/time and notes, then submit
- All diagnostic records are linked to specific patients

### PDF Export
- **Generate Report**: Click "Export PDF" button from patient list or patient view
- Report includes: Patient information, complete appointment history, all diagnostic records
- PDF is automatically downloaded

## Project Structure

```
mini project/
├── main.py              # Main Flask application
├── schema.sql           # Database schema
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── web_medical_management_project_report.pdf  # Project report
├── templates/          # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── patient_list.html
│   ├── patient_form.html
│   ├── patient_view.html
│   ├── appointment_list.html
│   ├── appointment_form.html
│   └── diagnostics.html
└── static/            # Static files (CSS, JS)
    └── (if any)
```

## Database

The system uses SQLite database stored in `data/medical.db`. The database is automatically created on first run using `schema.sql`.

### Database Schema

- **Patients Table**: id, first_name, last_name, dob, gender, contact
- **Appointments Table**: id, patient_id, appt_datetime, reason, status
- **Diagnostics Table**: id, patient_id, diag_datetime, notes

## System Requirements

- Python 3.7 or higher
- Flask 3.0.0 or higher
- FPDF2 2.7.6 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Notes

- The system operates entirely offline using local SQLite storage
- No internet connection required after installation
- All data is stored locally in the `data/` directory
- Sample data is automatically loaded on first run for demonstration
