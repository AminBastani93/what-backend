from django.core.management.base import BaseCommand
from products.models import Product
import random

class Command(BaseCommand):
    help = 'Populates the database with 30 sample products'

    def handle(self, *args, **kwargs):
        product_names = ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Camera', 'Smartwatch']
        brands = ['Apple', 'Samsung', 'Sony', 'Dell', 'LG', 'Asus']
        
        for i in range(30):
            name = f"{random.choice(brands)} {random.choice(product_names)} {i+1}"
            price = round(random.uniform(99.99, 1999.99), 2)
            stock = random.randint(0, 100)
            
            Product.objects.create(
                name=name,
                description=f"This is a sample description for {name}",
                price=price,
                stock=stock
            )
            
        self.stdout.write(self.style.SUCCESS('Successfully added 30 sample products'))
