from django.contrib import admin

# Register your models here.
from car_mechanic.models import *

admin.site.register(Mechanic)
admin.site.register(Order)