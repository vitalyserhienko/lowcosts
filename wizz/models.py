from django.db import models

# Create your models here.

class Airport(models.Model):
    name = models.CharField(max_length=100)
    counrty = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    iata_code = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class priceType(models.Model):
    name = models.CharField(max_length=100)
    priceType = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Price(models.Model):
    request_id = models.CharField(max_length=50)
    arrivalStation = models.CharField(max_length=100)
    arrivalStation_IATA = models.CharField(max_length=100)
    departureStation = models.CharField(max_length=100)
    departureStation_IATA = models.CharField(max_length=100)
    date = models.DateField()
    price = models.FloatField(null=True, blank=True, default=None)
    price_USD = models.FloatField(null=True, blank=True, default=None)
    currency = models.CharField(max_length=10)
    air_company = models.CharField(max_length=10)
    update_date = models.DateTimeField()
    price_type = models.CharField(max_length=20)

    # class Meta:
    #     ordering = ['price', '-update_date']

    def __str__(self):
        return self.arrivalStation + ' - ' + self.departureStation + ' // Вылет: ' + str(self.date) + ' // Дата обновления: ' + str(self.update_date)[0:16]

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
