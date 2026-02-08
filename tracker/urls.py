from django.urls import path
from . import views

urlpatterns = [
    # AUTH URLS (NEW)
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # CORE TRACKER URLS
    path('', views.tracker_view, name='tracker'),
    path('edit/<int:pk>/', views.edit_expense, name='edit_expense'),
    path('delete/<int:pk>/', views.delete_expense, name='delete_expense'),
    path('reports/', views.report_view, name='reports'),
]