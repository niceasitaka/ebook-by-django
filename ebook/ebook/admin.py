from django.contrib import admin
from .models import Books, RentHistory

# Register your models here.

admin.site.register(Books)
admin.site.register(RentHistory)