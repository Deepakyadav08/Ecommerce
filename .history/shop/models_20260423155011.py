from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    mobile_no = models.CharField(max_length=15)
    image_url = models.URLField(blank=True) 


    # image_url = models.ArrayField()
    
    def __str__(self):
        return self.name
    
class Order(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    address = models.TextField()
    Mobile_no = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"    
    
class Login(models.Model):
     email=models.CharField(max_length=100)
     password=models.CharField(max_length=50)

     def __str__(self):
         return self.email     
        