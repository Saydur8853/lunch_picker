
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api import  views


router = routers.DefaultRouter()
router.register(r'restaurants', views.RestaurantViewSet)
router.register(r'votes', views.VoteViewSet)
router.register(r'restaurant-winner', views.RestaurantWinnerViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/current_day_menu/', views.MenuViewSet.as_view(),name='get_current_day_menu'),
    
    # Authentication URLs
    path('api/register', views.RegisterView.as_view()),
    path('api/login', views.LoginView.as_view()),
    path('api/logout', views.LogoutView.as_view()),
    path('api/user', views.UserView.as_view())


]
