from django.contrib import admin

# Register your models here.
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'age', 'full_name', 'country']
    search_fields = ['username', 'email', 'age', 'full_name', 'country']
    list_filter = ['username', 'email', 'age', 'full_name', 'country']
    list_per_page = 10
    
admin.site.register(User,UserAdmin)
