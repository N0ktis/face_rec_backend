from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('', views.home, name='home'),
    path('add_user/<str:pk>', views.add_user, name='add_user'),
    path('update_user/', views.update_user, name='update_user'),
    path('delete_user/<str:pk>/', views.delete_user, name='delete_user'),
    path('profile/<str:pk>', views.user_profile, name='user_profile'),
    path('users/', views.browse_users, name='browse_users'),
    path('download/<str:pk>', views.export_users_csv, name='download'),
]
