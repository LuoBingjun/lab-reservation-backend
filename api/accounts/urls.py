from api.accounts import accounts
from django.urls import path

urlpatterns = [
    path(r'login', accounts.Login.as_view()),
    path(r'register', accounts.Register.as_view()),
    path(r'logout', accounts.Logout.as_view()),
    path(r'setpwd', accounts.Setpwd.as_view()),
    path(r'setinfo', accounts.Setinfo.as_view()),
]