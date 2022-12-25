from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:pk>/', views.show_pdf, name='show_pdf'),
    path('upload/', views.upload_document, name='upload'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_page, name='register')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)