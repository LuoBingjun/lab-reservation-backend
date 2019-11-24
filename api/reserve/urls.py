from api.reserve import reserve
from django.urls import path

urlpatterns = [
    path(r'queryused', reserve.QueryUsed.as_view()),
    path(r'submit', reserve.Submit.as_view()),
    path(r'specialsubmit', reserve.SpecialSubmit.as_view()),
    path(r'cancel', reserve.Cancel.as_view()),
    path(r'querysignin', reserve.QuerySignin.as_view()),
    path(r'signin', reserve.Signin.as_view()),
]