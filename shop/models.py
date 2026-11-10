from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    material = models.CharField(max_length=255, blank=True, default="")
    color = models.CharField(max_length=255, blank=True, default="")
    image_url = models.URLField(blank=True, default="")
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products"
    )
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="products")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name
