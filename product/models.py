from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(unique=True, max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or str(self.id)


class Product(models.Model):
    name = models.CharField(unique=True, max_length=25)
    category = models.ForeignKey(
        Category, blank=True, null=True, related_name="products",
        db_index=True,
                                 on_delete=models.SET_NULL)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        db_index=True
    )
    stock = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or str(self.id)
