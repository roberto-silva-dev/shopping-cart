from django.db import models
from django.db.models import UniqueConstraint
from users.models import CustomUser


class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user if self.user else self.session_key}'s cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity}x)"

    class Meta:
        constraints = [
            UniqueConstraint(fields=['cart', 'product'], name='uk_cartitem_cart_product'),
        ]
