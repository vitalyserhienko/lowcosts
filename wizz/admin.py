from django.contrib import admin
from .models import Airport, priceType, priceTemplate

# Register your models here.
admin.site.register(Airport)
admin.site.register(priceType)
admin.site.register(priceTemplate)
