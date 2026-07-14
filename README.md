# SafeX Solutions - Admin Subject Management (Week 2 Assignment)

## 1. Project Specifications
- **Group Allocation:** Group 44  
- **Component Built:** Admin Subject Management System Backend Module  
- **Core Functionality:** Create, Read, Update, and Delete academic courses and map them to the active teacher database.

## 2. Database Design Schema (SQL)
```sql
-- 1. Teachers Table
CREATE TABLE teachers (
    teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

-- 2. Subjects Table
CREATE TABLE subjects (
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_code TEXT UNIQUE NOT NULL,
    subject_name TEXT NOT NULL,
    credits INTEGER NOT NULL CHECK(credits >= 1 AND credits <= 6)
);

-- 3. Subject Assignments Table (Bridge Table)
CREATE TABLE subject_assignments (
    assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER,
    teacher_id INTEGER,
    assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id) ON DELETE CASCADE,
    UNIQUE(subject_id, teacher_id)
);
