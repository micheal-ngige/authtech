

from django.db import models

class Product(models.Model):
    STATUS_CHOICES = [
        ('genuine', 'Genuine'),
        ('fake', 'Fake'),
        ('used', 'Used'),
    ]

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='genuine')

    def last_used(self):
        last_transaction = Transaction.objects.filter(product=self).order_by('-timestamp').first()
        if last_transaction and last_transaction.status == 'used':
            return last_transaction.timestamp
        return None

    def __str__(self):
        return self.name


class Transaction(models.Model):
    STATUS_CHOICES = [
        ('genuine', 'Genuine'),
        ('fake', 'Fake'),
        ('used', 'Used'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    queried_by = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.product.name} - {self.status} at {self.timestamp}"
