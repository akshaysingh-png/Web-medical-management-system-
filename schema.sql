CREATE TABLE IF NOT EXISTS Patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    dob TEXT,
    gender TEXT,
    contact TEXT
);

CREATE TABLE IF NOT EXISTS Appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    appt_datetime TEXT NOT NULL,
    reason TEXT,
    status TEXT DEFAULT 'scheduled',
    FOREIGN KEY(patient_id) REFERENCES Patients(id)
);

CREATE TABLE IF NOT EXISTS Diagnostics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    diag_datetime TEXT NOT NULL,
    notes TEXT,
    FOREIGN KEY(patient_id) REFERENCES Patients(id)
);


