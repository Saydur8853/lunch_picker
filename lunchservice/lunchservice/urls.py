
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api import  views


router = routers.DefaultRouter()
router.register(r'restaurants', views.RestaurantViewSet)
# router.register(r'menus', views.MenuViewSet)
# router.register(r'employees', views.EmployeeViewSet)
router.register(r'votes', views.VoteViewSet)
# router.register(r'winners', views.WinnerViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # path('api/get_results', views.GetResultsView.as_view()),
    path('api/current_day_menu/', views.MenuViewSet.as_view(),name='get_current_day_menu'),

    path('api/get_results_for_current_day/', views.GetResultsForCurrentDayView.as_view(), name='get_results_for_current_day'),

    # Authentication URLs
    path('api/register', views.RegisterView.as_view()),
    path('api/login', views.LoginView.as_view()),
    path('api/logout', views.LogoutView.as_view()),
    path('api/user', views.UserView.as_view())


]
