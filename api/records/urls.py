from api.records import records
from django.urls import path

urlpatterns = [
    path(r'queryreserve', records.QueryReserve.as_view()),
    path(r'queryuse', records.QueryUse.as_view()),
    path(r'querybreach', records.QueryBreach.as_view()),
]