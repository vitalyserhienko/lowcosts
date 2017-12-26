from django import forms
import datetime
from datetime import timedelta
from .models import Airport, priceType, priceTemplate
from django.contrib.admin.widgets import AdminDateWidget

class FlightSearchForm(forms.Form):

    attrs_dict = { 'class': 'form-control', 'id': 'exampleFormControlSelect1' }

    def __init__(self, *args, **kwargs):
        super(FlightSearchForm, self).__init__(*args, **kwargs)
        self.fields['departureStation'].choices = [('', '! choose departure airport')] + [(lang.iata_code, lang.name) for lang in Airport.objects.all()]
        self.fields['arrivalStation'].choices = [('', '! choose arrival airport')] + [(lang.iata_code, lang.name) for lang in Airport.objects.all()]
        self.fields['priceType'].choices = [('', '! choose type of prices')] + [(pt.priceType, pt.name) for pt in priceType.objects.all()]

    departureStation = forms.ChoiceField(choices=(), widget=forms.Select(attrs=attrs_dict))
    arrivalStation = forms.ChoiceField(choices=(), widget=forms.Select(attrs=attrs_dict))
    date_from = forms.DateField(widget=forms.TextInput(attrs=
                                {
                                    'class': 'form-control',
                                    'type': 'date',
                                    'value': datetime.date.today()
                                }))
    date_to = forms.DateField(widget=forms.TextInput(attrs=
                                {
                                    'class': 'form-control',
                                    'type': 'date',
                                    'value': datetime.date.today() + datetime.timedelta(7)
                                }))

    departureStation_return = forms.CharField()
    arrivalStation_return = forms.CharField()
    date_from_return = forms.DateField(initial=datetime.date.today)
    date_to_return = forms.DateField(initial=datetime.date.today)

    priceType = forms.ChoiceField(choices=(), widget=forms.Select(attrs=attrs_dict))
