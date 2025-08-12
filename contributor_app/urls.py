from django.urls import path
from . import views

urlpatterns = [
    path('create/<str:content>/', views.create_data_entry, name='create'),
    path('view/', views.view_data_entries, name='view'),
    path('api/create_user/', views.CreateCustomUserView.as_view(), name='api_create_user'),
]