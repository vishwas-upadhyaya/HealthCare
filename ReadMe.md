# Healthcare Backend API

A Django REST Framework backend for a healthcare application that allows users to register, log in, and securely manage patient and doctor records.

## Features

- User authentication using JWT  
- Patient management (CRUD operations)  
- Doctor management (CRUD operations)  
- Patient-Doctor mapping functionality  
- Secure API endpoints with proper permissions  
- PostgreSQL database integration  

## API Endpoints

### Authentication

- POST `/api/auth/register/` — Register a new user (`name`, `email`, `password`)  
- POST `/api/auth/login/` — Log in a user and return a JWT token  
- POST `/api/auth/token/refresh/` — Refresh an expired JWT token  

### Patient Management

- POST `/api/patients/` — Add a new patient (Authenticated users only)  
- GET `/api/patients/` — Retrieve all patients created by the authenticated user  
- GET `/api/patients/<id>/` — Get details of a specific patient  
- PUT `/api/patients/<id>/` — Update patient details  
- DELETE `/api/patients/<id>/` — Delete a patient record  

### Doctor Management

- POST `/api/doctors/` — Add a new doctor (Authenticated users only)  
- GET `/api/doctors/` — Retrieve all doctors  
- GET `/api/doctors/<id>/` — Get details of a specific doctor  
- PUT `/api/doctors/<id>/` — Update doctor details  
- DELETE `/api/doctors/<id>/` — Delete a doctor record  

### Patient-Doctor Mapping

- POST `/api/mappings/` — Assign a doctor to a patient  
- GET `/api/mappings/` — Retrieve all patient-doctor mappings  
- GET `/api/mappings/patient/<patient_id>/` — Get all doctors assigned to a specific patient  
- DELETE `/api/mappings/<id>/` — Remove a doctor from a patient  

## Setup and Installation

1. Clone the repository:

    git clone <repository-url>
    cd healthcare_backend

2. Set up a virtual environment:

    python -m venv venv
    source venv/bin/activate    # On Windows, use: venv\Scripts\activate

3. Install dependencies:

    pip install -r requirements.txt

4. Configure environment variables:

    - Copy `.env.example` to `.env`
    - Fill in your PostgreSQL credentials and other configuration

5. Run migrations:

    python manage.py migrate

6. Run the development server:

    python manage.py runserver

## Environment Variables

Example entries for your `.env` file:

    SECRET_KEY=your_secret_key
    DEBUG=True
    DATABASE_URL=postgres://username:password@localhost:5432/dbname

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## Author

- [Vishwas Upadhyaya](https://github.com/vishwas-upadhyaya)