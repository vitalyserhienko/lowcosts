from django.contrib import admin
from .models import Airport, priceType, priceTemplate, Price

# Register your models here.
admin.site.register(Airport)
admin.site.register(priceType)
admin.site.register(priceTemplate)
admin.site.register(Price)
