import sqlite3

def connect_db():
    """Establishes connection and creates the student table with detailed columns if it doesn't exist."""
    conn = sqlite3.connect('students_records.db') # New database file for the new structure
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        school_name TEXT,
        class TEXT,
        division TEXT,
        mobile_number TEXT,
        email_id TEXT,
        father_name TEXT,
        address TEXT
    )
    ''')
    conn.commit()
    return conn

def add_student(details):
    """Adds a new student to the database using a dictionary of details."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO students (name, age, gender, school_name, class, division, mobile_number, email_id, father_name, address) 
        VALUES (:name, :age, :gender, :school_name, :class, :division, :mobile_number, :email_id, :father_name, :address)
    ''', details)
    conn.commit()
    conn.close()

def get_all_students():
    """Retrieves all students from the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    conn.close()
    return students

def update_student(student_id, details):
    """Updates the details of a specific student by their ID."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE students SET 
            name = :name, age = :age, gender = :gender, school_name = :school_name, 
            class = :class, division = :division, mobile_number = :mobile_number, 
            email_id = :email_id, father_name = :father_name, address = :address
        WHERE id = :id
    ''', {**details, 'id': student_id}) # Combine details dict with id
    conn.commit()
    conn.close()

def delete_student(student_id):
    """Deletes a student from the database by their ID."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
    conn.commit()
    conn.close()
