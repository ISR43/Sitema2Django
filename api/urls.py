from django.urls import path
from .views import CalculatorView, LogsView, frontend_view

urlpatterns = [
    path('', frontend_view, name='frontend'),
    path('api/calculate/', CalculatorView.as_view(), name='calculate'),
    path('api/log1/', LogsView.as_view(), name='logs'),
]
