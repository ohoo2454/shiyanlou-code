from django.contrib import admin

from .models import User, ConfirmString

# Register your models here.
admin.site.register([User, ConfirmString])
