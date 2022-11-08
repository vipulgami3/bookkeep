from django.urls import path
from BMS import views

urlpatterns = [
    path('add/', views.add),
    path('delete/<int:bid>', views.delete),
    path('edit/<int:bid>', views.edit),
    path('filter/', views.filter, name='filter'),
    path('search/', views.search, name='search'),
    path('all_user/', views.all_user, name='all_user'),
    path('all_superuser/', views.all_superuser, name='all_superuser'),
    path('all_deactive_user/', views.all_deactive_user, name='all_deactive_user'),
    path('add_user/', views.add_user, name='add_user'),
    path('deactivated_user/<int:uid>', views.deactivated_user, name='deactivated_user'),
    path('edit_user/<int:uid>', views.edit_user, name='edit_user'),
    path('activated_user/<int:uid>', views.activated_user, name='activated_user'),
]
