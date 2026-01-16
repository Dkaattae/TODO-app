from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('toggle/<int:todo_id>/', views.toggle_complete, name='toggle_complete'),
]