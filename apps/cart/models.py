from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

from apps.product.models import Product


##### ORDER


class Order(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='orders')
    customer = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 related_name='orders')
    total_cost = models.DecimalField(max_digits=100,
                                     decimal_places=2,
                                     default=0)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.product}- ordered by {self.customer}'

    def save(self, *args, **kwargs):
        self.total_cost = self.product.price * self.quantity
        super().save(*args, **kwargs)


class Cart(models.Model):
    CART_STATUS = (
        ('in_processing', 'in_processing'),
        ('completed', 'completed'),
        ('declined', 'declined')
    )
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='carts')
    status = models.CharField(choices=CART_STATUS,
                              default='in_processing',
                              max_length=20)

    def __str__(self):
        return self.user.email


class CartItem(models.Model):
    cart = models.ForeignKey(Cart,
                             on_delete=models.CASCADE,
                             related_name='cartitems')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='products')
    quantity = models.PositiveIntegerField()
    total_cost = models.DecimalField(max_digits=100,
                                     decimal_places=2,
                                     default=0)

    def __str__(self):
        return f'{self.cart.id} {self.product}'

    def save(self, *args, **kwargs):
        self.total_cost = self.product.price * self.quantity
        super(CartItem, self).save()
