from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Patient(models.Model):
    """Patient model for storing patient-related data"""
    # Patient information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ])
    
    # Contact information
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    
    # Medical information
    blood_type = models.CharField(max_length=5, blank=True, choices=[
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ])
    allergies = models.TextField(blank=True)
    medical_history = models.TextField(blank=True)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['-created_at']


class Doctor(models.Model):
    """Doctor model for storing doctor-related data"""
    # Doctor information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    # Professional information
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    
    # Contact information
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    email = models.EmailField()
    hospital = models.CharField(max_length=200, blank=True)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctors')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} ({self.specialization})"
    
    class Meta:
        ordering = ['last_name', 'first_name']


class PatientDoctorMapping(models.Model):
    """Model to map patients to their doctors"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='doctor_mappings')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='patient_mappings')
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('patient', 'doctor')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.patient} - {self.doctor}"
