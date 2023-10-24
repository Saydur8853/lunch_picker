from rest_framework import serializers
from .models import Employee, Restaurant, Menu, Vote


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "name", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validate_data):
        password = validate_data.pop("password", None)
        instance = self.Meta.model(**validate_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
        
class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    class Meta:
        model = Menu
        fields = ['id', 'date', 'items', 'price', 'restaurant', 'restaurant_name']



class VoteSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    restaurant_id = serializers.CharField(source='menu.restaurant.id', read_only=True)
    restaurant_name = serializers.CharField(source='menu.restaurant.name', read_only=True)
    items = serializers.CharField(source='menu.items', read_only=True)

    class Meta:
        model = Vote
        fields = ['id', 'employee_id', 'employee_name', 'restaurant_id', 'restaurant_name', "items", 'voted_at']
# class WinnerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Winner
#         fields = '__all__'
