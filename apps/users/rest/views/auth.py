from rest_framework_simplejwt.views import TokenObtainPairView
from ..serializers.auth import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT token view that enforces email verification
    """

    serializer_class = CustomTokenObtainPairSerializer
