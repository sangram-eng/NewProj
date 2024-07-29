from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    variation_name = models.CharField(max_length=100)
    name_area = models.CharField(max_length=100)

    def __str__(self):
        return f"User {self.user_id}"
