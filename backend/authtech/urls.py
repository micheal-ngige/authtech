
from django.urls import path
from .views import VerifyProductView

urlpatterns = [
    path('verify/', VerifyProductView.as_view(), name='verify_product'),
]
