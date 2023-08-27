from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializer import UserAccountSerializer
from .models import User

# Create your views here.
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = [AllowAny]
    
