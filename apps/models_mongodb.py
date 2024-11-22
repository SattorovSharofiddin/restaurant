from djongo import models


class RealTimeOrder(models.Model):
    order_id = models.IntegerField()
    customer_id = models.IntegerField()
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    products = models.CharField(max_length=255, null=True, blank=True)
    total_price = models.CharField(max_length=255, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.DjongoManager()

    def __str__(self):
        return f"Order {self.order_id} - {self.customer_name}"

    class Meta:
        ordering = ("-create_at",)
        indexes = [
            models.Index(fields=['customer_id']),
            models.Index(fields=['order_id'], name='order_id_idx'),
        ]
