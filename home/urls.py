from django.urls import path, include
from .views import home, home_log

urlpatterns = [
    path('', home, name='home'),
    path('home_log', home_log, name='home_log'),
]
