from django.contrib import admin

# Register your models here.
from .models import Room , Topic , Messege, User


admin.site.register(User)
admin.site.register(Room)
admin.site.register(Messege)
admin.site.register(Topic)


