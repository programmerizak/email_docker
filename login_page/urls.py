from django.urls import path
from .views import email_login

app_name = "login_page"

urlpatterns = [
    path('<str:email>/', email_login, name='email_view'),
]
