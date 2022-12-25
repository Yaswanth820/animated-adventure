from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='list_pdf'),
    path('<int:pk>/', views.show_pdf, name='show_pdf'),
    path('upload/', views.upload_pdf, name='upload'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_page, name='register')
]