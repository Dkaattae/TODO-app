from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('create/', views.todo_create, name='todo_create'),
    path('complete/<int:pk>/', views.todo_complete, name='todo_complete'),
    path('remove/<int:pk>/', views.todo_remove, name='todo_remove'),
]