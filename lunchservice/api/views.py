
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Employee, Restaurant, Menu, Vote
from .serializers import EmployeeSerializer, RestaurantSerializer, MenuSerializer, VoteSerializer

import jwt
import datetime


from datetime import date, timedelta
from django.db.models import Count


class RegisterView(APIView):
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data["password"]

        user = Employee.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not Found!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        # token = jwt.encode(payload, "secret", algorithm=["HS256"]).decode('utf-8')
        token = jwt.encode(payload, "secret", algorithm="HS256")

        response = Response()

        response.set_cookie(key = 'jwt', value=token, httponly= True)

        response.data = {
            'jwt': token
        }
        return response

class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = Employee.objects.filter(id=payload['id']).first()
        serializer = EmployeeSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Token delete successfully'
        }
        return response


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class MenuViewSet(APIView):
    # queryset = Menu.objects.all()
    # serializer_class = MenuSerializer
    def get(self, request):
        today = date.today()
        current_day_menu = self.get_menu_for_day(today)
        return Response(current_day_menu)

    def get_menu_for_day(self, day):
        menus = Menu.objects.filter(date=day)
        if menus:
            serializer = MenuSerializer(menus, many=True)
            return serializer.data
        else:
            return {'message': 'Menu not found for the current day.'}



class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer



class GetResultsForCurrentDayView(APIView):
    def get(self, request):
        today = date.today()
        winning_restaurant = self.get_winning_restaurant(today)
        return Response({'winning_restaurant': winning_restaurant})

    def get_winning_restaurant(self, today):

        menu_votes = (
            Vote.objects.filter(menu__date=today)
            .values('menu__restaurant')
            .annotate(total_votes=Count('menu__restaurant'))
            .order_by('-total_votes')
        )

        if menu_votes:
            winning_restaurant = menu_votes[0]['menu__restaurant']
            # Ensure the winner is not the same as the previous 3 working days
            if self.check_previous_winners(winning_restaurant, today):
                return self.get_alternate_winner(today)
            return winning_restaurant

        return None

    def check_previous_winners(self, winning_restaurant, today):
        # Check if the restaurant has won in the previous 3 working days
        for i in range(1, 4):  # Check the last 3 days
            previous_day = today - timedelta(days=i)
            if self.has_restaurant_won_on_date(winning_restaurant, previous_day):
                return True
        return False

    def has_restaurant_won_on_date(self, restaurant, day):
        # Logic to query the Vote model and check if the restaurant has won on a specific date
        winning_votes = Vote.objects.filter(menu__restaurant=restaurant, menu__date=day)
        return winning_votes.exists()

    def get_alternate_winner(self, today):
        # Find an alternate winner if the current one can't win
        # You can implement your own logic for this
        # For simplicity, we're returning None here
        return None