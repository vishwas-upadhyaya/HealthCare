from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        return False


class IsPatientOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a patient to access/modify their mappings
    """
    
    def has_object_permission(self, request, view, obj):
        # Check if the user is the one who created the patient
        if hasattr(obj, 'patient'):
            return obj.patient.created_by == request.user
        return False
