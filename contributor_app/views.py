from django.core.exceptions import PermissionDenied
from .models import UserProfile, DataEntry, CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import CustomUserSerializer

def check_user_role(user, is_manager_required=False):
    if not user.is_authenticated:
        raise PermissionDenied("کاربر وارد نشده.")
    profile = UserProfile.objects.get(user=user)
    if is_manager_required and not profile.is_manager:
        raise PermissionDenied("فقط مدیر می‌تواند این عملیات را انجام دهد.")
    return profile

def create_data_entry(request, content):
    user = request.user
    check_user_role(user)
    return DataEntry.objects.create(content=content, created_by=user)

def view_data_entries(request):
    user = request.user
    check_user_role(user)
    return DataEntry.objects.all()

class CreateCustomUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        check_user_role(request.user, is_manager_required=True)
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)