from __future__ import annotations
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from project.settings import DATABASES

schema = DATABASES.get("default").get("SCHEMA")


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Category(UUIDMixin):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "category"
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('name',)


class Subcategory(UUIDMixin):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "subcategory"
        verbose_name = _('subcategory')
        verbose_name_plural = _('subcategories')
        ordering = ('name',)


class Product(UUIDMixin):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    photo_link = models.URLField(blank=True, null=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "product"
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ('name',)


class CartItem(UUIDMixin):
    user_id = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    class Meta:
        db_table = "cart_item"
        verbose_name = _('cart_item')
        verbose_name_plural = _('cart_items')
        ordering = ('user_id',)


class Order(UUIDMixin):
    creation_dttm = models.DateTimeField(auto_now_add=True)
    user_id = models.CharField(max_length=255)
    address = models.TextField()
    payment_amount = models.DecimalField(max_digits=19, decimal_places=2)
    payment_link = models.URLField()

    def __str__(self):
        return f"Order {self.id} by {self.user_id}"

    class Meta:
        db_table = "order"
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        ordering = ('-creation_dttm',)
