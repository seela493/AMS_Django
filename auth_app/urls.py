from django.urls import path
from auth_app import views

urlpatterns = [
    path('', views.login_home, name= 'login'),
    path('admin_page/',views.admin_page, name="admin"),
    path('logout_admin/',views.logout_page, name="logout"),
    path('register_page/', views.register_page, name="register"),
]
