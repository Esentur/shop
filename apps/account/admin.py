from django.contrib import admin

# Register your models here.
from apps.account.models import CustomUser

############################################
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active')
############################################

admin.site.register(CustomUser,CustomUserAdmin)