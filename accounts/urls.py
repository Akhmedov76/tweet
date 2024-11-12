from django.urls import path

from accounts import views

app_name = 'auth'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('verify/email/', views.VerifyView.as_view(), name='verify'),

]
