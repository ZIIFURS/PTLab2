from django.db import models
from django.core.exceptions import ValidationError


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)  # количество на складе

    def __str__(self):
        return f"{self.name} ({self.quantity} шт.)"

    def can_be_purchased(self):
        return self.quantity > 0

    def decrease_quantity(self):
        if self.quantity <= 0:
            raise ValidationError("Товара нет в наличии")
        self.quantity -= 1
        self.save(update_fields=['quantity'])


class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    person = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.person} купил {self.product.name}"