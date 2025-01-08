from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    """
    Product model representing items in the database
    """
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    selected_by = models.ManyToManyField(
        User, 
        related_name='selected_products',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name