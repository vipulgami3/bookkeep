from django.urls import path
from BMS import views

urlpatterns = [
    path('add/', views.add),
    path('delete/<int:bid>', views.delete),
    path('edit/<int:bid>', views.edit),
    path('filter/', views.filter, name='filter'),
    path('search/', views.search, name='search'),
]
