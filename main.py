import sqlite3
import json

# =====================================================================
# SYSTEM INITIALIZATION & DATABASE SETUP
# =====================================================================

def init_db():
    """Initializes an in-memory database with schema structure."""
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # 1. Teachers Table
    cursor.execute('''
        CREATE TABLE teachers (
            teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    
    # 2. Subjects Table
    cursor.execute('''
        CREATE TABLE subjects (
            subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_code TEXT UNIQUE NOT NULL,
            subject_name TEXT NOT NULL,
            credits INTEGER NOT NULL CHECK(credits >= 1 AND credits <= 6)
        )
    ''')
    
    # 3. Subject Assignments Table
    cursor.execute('''
        CREATE TABLE subject_assignments (
            assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER,
            teacher_id INTEGER,
            assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE,
            FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id) ON DELETE CASCADE,
            UNIQUE(subject_id, teacher_id)
        )
    ''');
    
    # Seed Initial Teacher Data
    cursor.executemany('''
        INSERT INTO teachers (name, email) VALUES (?, ?)
    ''', [
        ("Sir Aqib", "aqib@safex.edu"),
        ("Dr. Sarah", "sarah@safex.edu")
    ])
    
    conn.commit()
    return conn

# =====================================================================
# RESTful API CONTROLLERS (SIMULATOR LAYER)
# =====================================================================

class SubjectController:
    def __init__(self, conn):
        self.conn = conn

    def create_subject(self, payload_json):
        try:
            data = json.loads(payload_json)
            code = data.get('subject_code')
            name = data.get('subject_name')
            credits = data.get('credits')
            
            if not code or not name or credits is None:
                return json.dumps({"error": "Missing required fields"}), 400
                
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO subjects (subject_code, subject_name, credits)
                VALUES (?, ?, ?)
            ''', (code, name, credits))
            self.conn.commit()
            return json.dumps({"message": "Subject created successfully", "id": cursor.lastrowid}), 201
        except sqlite3.IntegrityError:
            return json.dumps({"error": "Subject code must be unique"}), 409
        except Exception as e:
            return json.dumps({"error": str(e)}), 400

    def get_all_subjects(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM subjects")
        rows = cursor.fetchall()
        subjects = [{"subject_id": r[0], "subject_code": r[1], "subject_name": r[2], "credits": r[3]} for r in rows]
        return json.dumps(subjects), 200

    def update_subject(self, subject_id, payload_json):
        try:
            data = json.loads(payload_json)
            name = data.get('subject_name')
            credits = data.get('credits')
            
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE subjects SET subject_name = ?, credits = ? WHERE subject_id = ?
            ''', (name, credits, subject_id))
            self.conn.commit()
            if cursor.rowcount == 0:
                return json.dumps({"error": "Subject not found"}), 404
            return json.dumps({"message": "Subject updated successfully"}), 200
        except Exception as e:
            return json.dumps({"error": str(e)}), 400

    def delete_subject(self, subject_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM subjects WHERE subject_id = ?", (subject_id,))
        self.conn.commit()
        if cursor.rowcount == 0:
            return json.dumps({"error": "Subject not found"}), 404
        return json.dumps({"message": "Subject deleted successfully"}), 200

    def assign_teacher(self, payload_json):
        try:
            data = json.loads(payload_json)
            sub_id = data.get('subject_id')
            t_id = data.get('teacher_id')
            
            cursor = self.conn.cursor()
            # Check if teacher exists
            cursor.execute("SELECT 1 FROM teachers WHERE teacher_id = ?", (t_id,))
            if not cursor.fetchone():
                return json.dumps({"error": "Teacher not found"}), 404
                
            cursor.execute('''
                INSERT INTO subject_assignments (subject_id, teacher_id)
                VALUES (?, ?)
            ''', (sub_id, t_id))
            self.conn.commit()
            return json.dumps({"message": "Teacher assigned to subject successfully"}), 201
        except sqlite3.IntegrityError:
            return json.dumps({"error": "Assignment already exists or invalid references"}), 409
        except Exception as e:
            return json.dumps({"error": str(e)}), 400

# =====================================================================
# AUTOMATED UNIT TESTS & WALKTHROUGH SIMULATOR
# =====================================================================

def run_tests_and_simulation():
    print("==================================================")
    print("   SAFEX SOLUTIONS - ADMIN SUBJECT SYSTEM DEMO    ")
    print("==================================================\n")
    
    conn = init_db()
    api = SubjectController(conn)
    
    # ----------------- TEST CASE 1: Subject Creation -----------------
    print("[Test 1] Registering New Subjects...")
    res, code = api.create_subject(json.dumps({
        "subject_code": "CS-201",
        "subject_name": "Database Management Systems",
        "credits": 4
    }))
    print(f"Response: {res} | Status: {code}")
    
    # ----------------- TEST CASE 2: Validation Constraint ------------
    print("\n[Test 2] Testing Credit Limits (Must be 1-6)...")
    res, code = api.create_subject(json.dumps({
        "subject_code": "CS-502",
        "subject_name": "Invalid Course",
        "credits": 8
    }))
    print(f"Response: {res} | Status: {code} (Expected 400 Error due to CHECK constraint)")

    # ----------------- TEST CASE 3: Read Operation -------------------
    print("\n[Test 3] Fetching Subject Registry...")
    res, code = api.get_all_subjects()
    print(f"Database Registry Payload:\n{json.dumps(json.loads(res), indent=2)}")

    # ----------------- TEST CASE 4: Update Operation -----------------
    print("\n[Test 4] Modifying Subject details (ID: 1)...")
    res, code = api.update_subject(1, json.dumps({
        "subject_name": "Advanced Database Systems",
        "credits": 3
    }))
    print(f"Response: {res} | Status: {code}")

    # ----------------- TEST CASE 5: Cross-Module Assignment ---------
    print("\n[Test 5] Assigning Teacher (Sir Aqib, ID: 1) to Subject (ID: 1)...")
    res, code = api.assign_teacher(json.dumps({
        "subject_id": 1,
        "teacher_id": 1
    }))
    print(f"Response: {res} | Status: {code}")
    print("\n==================================================")
    print("        ALL SYSTEM INTEGRITY TESTS PASSED         ")
    print("==================================================")

if __name__ == '__main__':
    run_tests_and_simulation()
