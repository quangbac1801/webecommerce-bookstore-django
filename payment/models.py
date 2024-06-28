from django.db import models

from myapp.models import Order
# Create your models here.
class PaymentVnpay(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_desc = models.TextField()
    vnp_TransactionNo = models.CharField(max_length=255, blank=True, null=True)
    vnp_ResponseCode = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment for Order {self.order.id}'
