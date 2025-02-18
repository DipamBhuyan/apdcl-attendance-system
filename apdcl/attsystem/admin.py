from django.contrib import admin
from .models import CustomUser,attendance,holiday_list

admin.site.register(CustomUser)
admin.site.register(attendance)
admin.site.register(holiday_list)
# Register your models here.
