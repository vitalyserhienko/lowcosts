from django.db import models

# Create your models here.

class Airport(models.Model):
    name = models.CharField(max_length=100)
    counrty = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    iata_code = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class priceType(models.Model):
    name = models.CharField(max_length=100)
    priceType = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class priceTemplate(models.Model):
    templete_name = models.CharField(max_length=100)
    departureStation = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departureAirport')
    arrivalStation = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrivalAirport')
    date_from = models.DateField()
    date_to = models.DateField()
    departureStation_return = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departureAirport_return')
    arrivalStation_return = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrivalAirport_return')
    date_from_return = models.DateField()
    date_to_return = models.DateField()
    priceType = models.ForeignKey(priceType, on_delete=models.CASCADE)

    def __str__(self):
        return self.templete_name
