from django.contrib import admin
from .models import Restaurant, Menu, Employee, Vote, Winner

class MenuInline(admin.TabularInline):
    model = Menu

class RestaurantAdmin(admin.ModelAdmin):
    inlines = [MenuInline]

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Employee)
admin.site.register(Vote)
admin.site.register(Winner)
