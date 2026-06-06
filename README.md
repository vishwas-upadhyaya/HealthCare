# Project Name
HealthCare Backend (HealthCare repository)

## Project Overview
This project is a backend RESTful API built for managing healthcare records, specifically focused on patient and doctor management. It provides endpoints for user registration, patient profiling, doctor details, and the assignment (mapping) of patients to their respective doctors. The API is secured using JWT authentication to ensure that healthcare records remain private and accessible only by authorized users.

## Deep Technical Details (Architecture, Pipeline, Loss, Optimizer)

### Architecture
- **Framework:** Django 4.2.8 coupled with Django REST Framework 3.14.0.
- **Design Pattern:** MVC (Model-View-Controller) adapted as MVT (Model-View-Template/API Views).
- **Database:** PostgreSQL (via `psycopg2-binary`).
- **Authentication:** JSON Web Tokens (JWT) through `djangorestframework-simplejwt`.
- **API Structure:**
  - **Models:** Relational structure containing `Patient`, `Doctor`, and `PatientDoctorMapping`.
  - **ViewSets:** `ModelViewSet` instances handles automatic CRUD routing for entities (`PatientViewSet`, `DoctorViewSet`, `PatientDoctorMappingViewSet`).
  - **Permissions:** Custom object-level permissions such as `IsOwnerOrReadOnly` and `IsPatientOwner` restrict operations so users can only modify data they created.

### Data Pipeline
- **Validation:** Utilizes Django's `RegexValidator` for phone number validation and `EmailField` for standardizing emails.
- **Serialization:** DRF Serializers convert complex Model instances to native Python datatypes for JSON rendering.
- **Environment Variables:** Handled via `python-decouple` to ensure security parameters (like secret keys and database URLs) aren't hardcoded.

### Loss & Optimizer
*Note: This repository contains backend web development code rather than a Deep Learning model. As such, standard Neural Network components like Loss Functions and Optimizers do not apply here.*

## Why it was done
The project acts as a secure, foundational backend system for healthcare providers. It was developed to streamline the administration of medical data, map patient-doctor relationships, and provide a secure, authenticated API that frontend applications can reliably consume.

## Tech Stack
- **Python** (Language)
- **Django** (Web Framework)
- **Django REST Framework** (API Framework)
- **PostgreSQL** (Relational Database via psycopg2)
- **SimpleJWT** (Authentication)
- **django-cors-headers** (CORS management)
- **python-decouple** (Environment configuration)
