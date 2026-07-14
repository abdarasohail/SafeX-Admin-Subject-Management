# SafeX Solutions - Admin Subject Management (Week 2 Assignment)

## 1. Project Specifications
- **Group Allocation:** Group 44  
- **Component Built:** Admin Subject Management System Backend Module  
- **Core Functionality:** Create, Read, Update, and Delete academic courses and map them to the active teacher database.

## 2. API Design Specification Details
The architecture exposes clean RESTful simulation design boundaries:
- `POST /api/v1/subjects` - Registers a new subject with schema payload verification.
- `GET /api/v1/subjects` - Lists all courses within the database context.
- `PUT /api/v1/subjects/{id}` - Updates information properties matching a given entity key.
- `DELETE /api/v1/subjects/{id}` - Purges the targeted course row and cascades down dependencies.
- `POST /api/v1/assignments` - Binds a valid cross-module unique teacher record to a designated subject.

## 3. Database Architecture Strategy
The system runs a fully relational 3-table relational design logic enforcing data integrity at the hardware engine layer:
- **Teachers Table:** Holds tracking profiles.
- **Subjects Table:** Protects business keys via a unique code check restriction constraint.
- **Subject Assignments Table:** Resolves a classic Many-to-Many entity map problem using foreign key constraints linked with an internal structural unique paired restriction constraint.
