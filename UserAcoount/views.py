from rest_framework import generics, status, response
from rest_framework.permissions import AllowAny

from .serializer import UserAccountSerializer, UserAccountLoginSerializer
from .models import User


# Create your views here.
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = [AllowAny]


class UserLogin(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserAccountLoginSerializer

    def post(self, request, *args, **kwargs):
        data = super().create(request, *args, **kwargs)
        return response.Response(status=status.HTTP_200_OK, data=data.data)
