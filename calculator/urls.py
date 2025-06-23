from django.urls import path
from .views import salary_calculator

urlpatterns = [
    path('', salary_calculator, name='salary_calculator'),
]
