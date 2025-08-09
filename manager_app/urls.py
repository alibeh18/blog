from django.urls import path
from . import views

urlpatterns = [
    path('create/<str:content>/', views.create_data_entry, name='create'),
    path('edit/<int:entry_id>/<str:new_content>/', views.edit_data_entry, name='edit'),
    path('delete/<int:entry_id>/', views.delete_data_entry, name='delete'),
    path('view/', views.view_data_entries, name='view'),
]