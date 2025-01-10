from django.urls import path
from auth_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_home, name= 'login'),
    path('admin-page/',views.admin_page, name="admin"),
    path('logout-admin/',views.logout_page, name="logout"),
    path('register-page/', views.register_page, name="register"),
    path('teacher-detail/',views.teacher_detail, name="teacher"),
    path('image/',views.teacher_image, name="image"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
