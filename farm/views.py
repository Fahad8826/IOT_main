
# views.py
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Farm
from .serializers import FarmSerializer


class IsAdminOrManagerOrOwner(permissions.BasePermission):
    """
    Custom permission for role-based access:
    - Admins can access all farms
    - Managers can access all farms
    - Regular users can only access their own farms
    """

    def has_object_permission(self, request, view, obj):
        # Allow admins and managers full access
        if request.user.role in ['admin', 'manager']:
            return True
        # Regular users can only access their own farms
        return obj.owner == request.user




class FarmListCreateView(generics.ListCreateAPIView):
    """
    List all farms or create a new farm.
    Admins and managers can specify the owner, while regular users are automatically assigned as the owner.
    """
    serializer_class = FarmSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrManagerOrOwner]

    def get_queryset(self):
        """
        Return all farms for admins/managers, or only user's farms for regular users.
        """
        user = self.request.user
        if user.role in ['admin', 'manager']:
            return Farm.objects.all()
        return Farm.objects.filter(owner=user)

    def perform_create(self, serializer):
        """
        Allow admins/managers to specify owner, otherwise set to current user.
        """
        user = self.request.user

        if user.role in ['admin', 'manager']:
            # Admins and managers can specify the owner
            owner_id = self.request.data.get('owner')
            if owner_id:
                # Save the farm with the specified owner
                serializer.save(owner_id=owner_id)
            else:
                # If no owner is specified, default to the current user
                serializer.save(owner=user)
        else:
            # Regular users can only create farms for themselves
            serializer.save(owner=user)


class FarmDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a farm instance
    """
    serializer_class = FarmSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrManagerOrOwner]

    def get_queryset(self):
        """
        Return all farms for admins/managers, or only user's farms for regular users
        """
        user = self.request.user
        if user.role in ['admin', 'manager']:
            return Farm.objects.all()
        return Farm.objects.filter(owner=user)


from django.shortcuts import render

def create_farm_page(request):
    return render(request, 'create_farm.html')

from django.shortcuts import render
from rest_framework import generics
from .models import Farm, Motor, Valve
from .serializers import FarmSerializer, MotorSerializer, ValveSerializer
from rest_framework.permissions import IsAuthenticated

class FarmListCreateView(generics.ListCreateAPIView):
    serializer_class = FarmSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Farm.objects.filter(user=self.request.user)

class FarmDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FarmSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Farm.objects.filter(user=self.request.user)

class MotorListCreateView(generics.ListCreateAPIView):
    serializer_class = MotorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        farm_id = self.kwargs.get('farm_id')
        return Motor.objects.filter(farm_id=farm_id, farm__user=self.request.user)

class MotorDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MotorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        farm_id = self.kwargs.get('farm_id')
        return Motor.objects.filter(farm_id=farm_id, farm__user=self.request.user)

class ValveListCreateView(generics.ListCreateAPIView):
    serializer_class = ValveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        motor_id = self.kwargs.get('motor_id')
        return Valve.objects.filter(motor_id=motor_id, motor__farm__user=self.request.user)

class ValveDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ValveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        motor_id = self.kwargs.get('motor_id')
        return Valve.objects.filter(motor_id=motor_id, motor__farm__user=self.request.user)
# -----------------------------html-------------------------------

# def farm_management(request, user_id=None):  # Add user_id as an optional argument
#     return render(request, 'farmCRUD.html', {'user_id': user_id})

def farm_management(request):  # Add user_id as an optional argument
    return render(request, 'farmCRUD.html', )

