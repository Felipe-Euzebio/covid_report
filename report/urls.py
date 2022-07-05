from django.urls import path
from .views import show_report

urlpatterns = [
    path('', show_report, name="show_report")
]
