from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import User, Product

class UserModelAdmin(UserAdmin):
    model=User
    list_display=["id",'email','name','is_active','is_superuser','is_staff','is_customer','is_seller']
    list_filter=['is_superuser']

    fieldsets = (
        ("User Credentials", {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("name","city")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "is_customer", "is_seller","groups", "user_permissions")})
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "name", "password1", "password2", "is_active", "is_staff", "is_superuser", "is_customer", "is_seller"),
        }),
    )
    search_fields=["email"]
    ordering=["email","id"]
    filter_horizontal=[]

# Register your models here.
admin.site.register(User,UserModelAdmin)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "stock")
    search_fields = ("name",)