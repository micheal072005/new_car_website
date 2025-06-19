from django.db import models
from django.contrib.auth.models import User



# Brand model to store car brands
class Brand(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)

    def __str__(self):
        return self.name


# Car model to store car details
class Car(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
    ]

    TRANSMISSION_CHOICES = [
        ('automatic', 'Automatic'),
        ('manual', 'Manual'),
    ]

    FUEL_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ]

    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='cars')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    year_of_manufacture = models.PositiveIntegerField()
    mileage = models.PositiveIntegerField(help_text="Mileage in kilometers")
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='used')
    transmission = models.CharField(max_length=10, choices=TRANSMISSION_CHOICES, default='manual')
    fuel_type = models.CharField(max_length=10, choices=FUEL_CHOICES, default='petrol')
    engine_capacity = models.DecimalField(max_digits=4, decimal_places=1, help_text="Engine capacity in liters")
    color = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to='car_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.brand.name}"


# Car image model to store multiple images for a car
class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='car_gallery/')

    def __str__(self):
        return f"Image for {self.car.name}"
    

# Cart model
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    total_price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"


# Cart item model to store car items added to the cart
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.car.name} in {self.cart.user.username}'s cart"


# Contact us model
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.email}"
    

# Purchase model to store purchase details
class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='purchases')
    full_name = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100)
    proof_of_payment = models.ImageField(upload_to='payment_proofs/', blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    date_purchased = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')

    def total_amount(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.car.name} purchased by {self.user.username}"
    



