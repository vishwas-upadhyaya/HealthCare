from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Patient, Doctor, PatientDoctorMapping


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password', 'password_confirm')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True}
        }
    
    def validate(self, attrs):
        """Validate that passwords match"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        """Create and return a new user"""
        validated_data.pop('password_confirm')
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class PatientSerializer(serializers.ModelSerializer):
    """Serializer for the Patient model"""
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at', 'created_by_username')
    
    def create(self, validated_data):
        """Create and return a new patient, set the created_by field to the current user"""
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class DoctorSerializer(serializers.ModelSerializer):
    """Serializer for the Doctor model"""
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = Doctor
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at', 'created_by_username')
    
    def create(self, validated_data):
        """Create and return a new doctor, set the created_by field to the current user"""
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    """Serializer for the PatientDoctorMapping model"""
    patient_name = serializers.ReadOnlyField(source='patient.__str__')
    doctor_name = serializers.ReadOnlyField(source='doctor.__str__')
    
    class Meta:
        model = PatientDoctorMapping
        fields = '__all__'
        read_only_fields = ('created_at',)
    
    def validate(self, attrs):
        """Validate that the user has permission to map this patient"""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            # Check if the user has permission to assign this patient
            if attrs['patient'].created_by != request.user:
                raise serializers.ValidationError({
                    "patient": "You don't have permission to assign doctors to this patient."
                })
        return attrs


class PatientDoctorMappingDetailSerializer(PatientDoctorMappingSerializer):
    """Detailed serializer for PatientDoctorMapping including nested doctor information"""
    doctor = DoctorSerializer(read_only=True)
