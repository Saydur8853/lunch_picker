
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Employee, Restaurant, Menu, Vote, Winner
from .serializers import EmployeeSerializer, RestaurantSerializer, MenuSerializer, VoteSerializer, RestaurantWinnerSerializer
from django.db.models import Avg
import jwt
import datetime
from django.utils import timezone


from datetime import date


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



def is_now_in_time_period(start_time, end_time, now_time):
    if start_time < end_time:
        return start_time <= now_time <= end_time
    else:
        return now_time >= start_time or now_time <= end_time

def calculate_winner(today):
    queryset = Vote.objects.filter(voted_at__date=today).values('menu__restaurant_id') \
        .annotate(avg_score=Avg('score')).order_by('-avg_score')

    if not queryset:
        return None, None

    winner_list = Winner.objects.filter().order_by('-winning_date')
    final_winner = Restaurant.objects.get(id=queryset[0]['menu__restaurant_id'])
    avg_score = queryset[0]['avg_score']
    
    if len(winner_list) > 2:
        for restaurant_data in queryset:
            restaurant_id = restaurant_data['menu__restaurant_id']
            
            if winner_list[0].restaurant_id != restaurant_id and winner_list[1].restaurant_id != restaurant_id:
                final_winner = Restaurant.objects.get(id=restaurant_id)
                avg_score = restaurant_data['avg_score']
                break
    return final_winner, avg_score

def create_winner(today, final_winner, avg_score):
    winner_obj = Winner.objects.create(restaurant=final_winner, winning_date=today)
    winner_obj.menu_set.add(final_winner.menu_set.filter(date=today).first())
    winner_obj.avg_score = avg_score
    winner_obj.save()
    return winner_obj

class RestaurantWinnerViewSet(viewsets.ViewSet):
    queryset = Winner.objects.all()
    serializer_class = RestaurantWinnerSerializer

    def list(self, request):
        today = timezone.now().date()
        
        try:
            winner = Winner.objects.get(winning_date=today)
            serializer = RestaurantWinnerSerializer(winner)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Winner.DoesNotExist:
            print("Not Calculated Yet")

        if is_now_in_time_period(timezone.make_time(12, 10), timezone.make_time(23, 59), timezone.now().time()):
            final_winner, avg_score = calculate_winner(today)
            
            if final_winner is None:
                return Response("No Voting Happened Today", status=status.HTTP_200_OK)
            
            winner_obj = create_winner(today, final_winner, avg_score)
            
            serializer = RestaurantWinnerSerializer(winner_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("There is Still Voting Time Left, Try Between 12:10 PM - 11:59 AM",
                            status=status.HTTP_406_NOT_ACCEPTABLE)

