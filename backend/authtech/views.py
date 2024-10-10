# authtech/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Product, Transaction
from .serializers import ProductSerializer, TransactionSerializer

class VerifyProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_code = request.data.get('product_code')
        querying_service = request.user.username

        try:
            product = Product.objects.get(code=product_code)
            last_used_timestamp = product.last_used()
            if last_used_timestamp:
                status_message = f"used at {last_used_timestamp}"
            else:
                status_message = product.status
        except Product.DoesNotExist:
            status_message = 'unknown'

        transaction = Transaction.objects.create(
            product=product if 'product' in locals() else None,
            status=status_message if 'product' in locals() else 'unknown',
            queried_by=querying_service
        )

        return Response({'status': status_message}, status=status.HTTP_200_OK)
