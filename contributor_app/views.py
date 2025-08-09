from django.core.exceptions import PermissionDenied
from .models import UserProfile, DataEntry

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