from django.http import JsonResponse
from rest_framework import viewsets
from .permissions import IsAdmin, IsFaculty, IsLecturer, IsStudent
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]  # sadece admin erişebilsin
