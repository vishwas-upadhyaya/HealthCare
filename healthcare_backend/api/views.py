from rest_framework import viewsets, generics, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import (
    UserRegistrationSerializer, 
    PatientSerializer, 
    DoctorSerializer, 
    PatientDoctorMappingSerializer,
    PatientDoctorMappingDetailSerializer
)
from .permissions import IsOwnerOrReadOnly, IsPatientOwner


class UserRegistrationView(generics.CreateAPIView):
    """API view for user registration"""
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer


class PatientViewSet(viewsets.ModelViewSet):
    """ViewSet for Patient model, provides CRUD operations for patients"""
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email', 'phone_number']
    
    def get_queryset(self):
        """Returns only patients created by the authenticated user"""
        return Patient.objects.filter(created_by=self.request.user)


class DoctorViewSet(viewsets.ModelViewSet):
    """ViewSet for Doctor model, provides CRUD operations for doctors"""
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'specialization', 'hospital']
    
    def get_queryset(self):
        """Return all doctors, but ensure only creators can edit their entries"""
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return Doctor.objects.filter(created_by=self.request.user)
        return Doctor.objects.all()


class PatientDoctorMappingViewSet(viewsets.ModelViewSet):
    """ViewSet for PatientDoctorMapping model"""
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated, IsPatientOwner]
    
    def get_queryset(self):
        """Returns all mappings for patients created by the authenticated user"""
        return PatientDoctorMapping.objects.filter(patient__created_by=self.request.user)
    
    @action(detail=False, methods=['get'], url_path='patient/(?P<patient_id>[^/.]+)')
    def get_patient_doctors(self, request, patient_id=None):
        """Get all doctors for a specific patient"""
        # Ensure the user has permission to access this patient's data
        patient = get_object_or_404(Patient, id=patient_id, created_by=request.user)
        
        mappings = PatientDoctorMapping.objects.filter(patient=patient)
        serializer = PatientDoctorMappingDetailSerializer(mappings, many=True)
        return Response(serializer.data)
