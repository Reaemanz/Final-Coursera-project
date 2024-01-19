from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser, Group
#from django.db import models

class CustomUser(AbstractUser):
    # Custom User model to include additional fields if needed
    pass

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(MenuItem, through='OrderItem')
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"Order #{self.pk} - {self.customer.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Additional profile fields for managers or delivery crew
    is_manager = models.BooleanField(default=False)
    is_delivery_crew = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
