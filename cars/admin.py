from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Car)
admin.site.register(Brand)
admin.site.register(CarImage)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Purchase)