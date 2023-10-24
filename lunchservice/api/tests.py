from django.test import TestCase
from .models import Restaurant

class RestaurantModelTest(TestCase):
    def test_create_restaurant(self):
        restaurant = Restaurant(name="My Restaurant", description="A great place to eat")
        restaurant.save()

        self.assertEqual(restaurant.name, "My Restaurant")
        self.assertEqual(restaurant.description, "A great place to eat")



from .serializers import MenuSerializer

class MenuSerializerTest(TestCase):
    def test_menu_serializer(self):
        menu = Menu(restaurant_id=1, date="2023-10-20", items=["Burger", "Fries"])
        serializer = MenuSerializer(instance=menu)
        data = serializer.data

        self.assertEqual(data['restaurant_id'], 1)
        self.assertEqual(data['date'], "2023-10-20")
        self.assertEqual(data['items'], ["Burger", "Fries"])

from rest_framework.test import APITestCase
from .serializers import RestaurantSerializer

class RestaurantViewSetTest(APITestCase):
    def test_list_restaurants(self):
        restaurant = Restaurant(name="Test Restaurant", description="A test place")
        restaurant.save()

        response = self.client.get('/api/restaurants/')
        data = response.data
        serializer = RestaurantSerializer(restaurant)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, [serializer.data])