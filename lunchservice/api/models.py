from django.db import models
from django.contrib.auth.models import AbstractUser


class Employee(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return f"{self.name} ({self.username}) - {self.email}"

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateField()
    items = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"Menu for {self.restaurant.name} on {self.date}"

    


class Vote(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.username} voted for {self.menu.restaurant.name} menu on {self.voted_at}"

# class Winner(models.Model):
#     restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
#     date = models.DateField()
#     consecutive_wins = models.PositiveIntegerField(default=1)
#     # Add more fields like number of consecutive wins, etc.

#     def __str__(self):
#         return f"Winner for {self.date}: {self.restaurant.name}"