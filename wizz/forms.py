from django import forms
import datetime
from .models import Airport, priceType, priceTemplate

class FlightSearchForm(forms.Form):
    departureStation = forms.CharField()
    arrivalStation = forms.CharField()
    date_from = forms.DateField(initial = datetime.date.today)
    date_to = forms.DateField(initial=datetime.date.today)
    departureStation_return = forms.CharField()
    arrivalStation_return = forms.CharField()
    date_from_return = forms.DateField(initial=datetime.date.today)
    date_to_return = forms.DateField(initial=datetime.date.today)
    priceType = forms.CharField()
