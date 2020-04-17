from django.urls import path
from .views import home, countryData

urlpatterns = [
    path('', home, name="home"),
    path('countryData', countryData, name="countryData")
]
