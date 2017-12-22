from django.shortcuts import render
from .models import Airport, priceType, priceTemplate, Price
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import FlightSearchForm
from .wizz_request import request_data
from django.utils import timezone
import requests
import json

# Create your views here.
def home(request):
    return render(request, 'base.html', {})
    
def search_history(request):
    prices = Price.objects.all().order_by('update_date', 'price_USD')
    paginator = Paginator(prices, 25)
    page = request.GET.get('page')
    try:
        prices = paginator.page(page)
    except PageNotAnInteger:
        prices = paginator.page(1)
    except EmptyPage:
        prices = paginator.page(paginator.num_pages)
    # contacts = paginator.get_page(page)
    return render(request, 'wizz/history.html', { 'prices': prices })

def flight_search_form(request):

    form = FlightSearchForm(request.POST)
    request_res = {}

    if request.method == 'POST':
        departureStation = request.POST.get('departureStation')
        arrivalStation = request.POST.get('arrivalStation')
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        priceType = request.POST.get('priceType')
        request_1 = request_data(departureStation, arrivalStation, date_from, date_to, priceType)

        currency_now = requests.get('https://openexchangerates.org/api/latest.json?app_id=6cdf29a6391b479cb9d0a4fe9608fa04')
        currency_json = json.loads(currency_now.content)

        for j in request_1['outboundFlights']:
            new_price = Price()
            new_price.departureStation_IATA = j['departureStation']
            new_price.arrivalStation_IATA = j['arrivalStation']
            new_price.date = j['departureDate'][0:10]
            if j['price'] is None:
                print(j['price'])
                new_price.price = 0.0
                new_price.currency = 'NON'
                new_price.price_USD = 0.0
            else:
                new_price.price = j['price']['amount']
                new_price.currency = j['price']['currencyCode']
                new_price.price_USD = float(new_price.price)/currency_json['rates'][new_price.currency]
            new_price.price_type = priceType
            new_price.update_date = timezone.now()
            airport_d = Airport.objects.get(iata_code=j['departureStation'])
            airport_a = Airport.objects.get(iata_code=j['arrivalStation'])
            new_price.departureStation = airport_d.name #j['departureStation']
            new_price.arrivalStation = airport_a.name #j['arrivalStation']
            new_price.air_company = 'WiZZ Air'
            new_price.save()

        for j in request_1['returnFlights']:
            new_price_return = Price()
            new_price_return.departureStation_IATA = j['departureStation']
            new_price_return.arrivalStation_IATA = j['arrivalStation']
            new_price_return.date = j['departureDate'][0:10]
            if j['price'] is None:
                print(j['price'])
                new_price_return.price = 0.0
                new_price_return.currency = 'NON'
                new_price_return.price_USD = 0.0
            else:
                new_price_return.price = j['price']['amount']
                new_price_return.currency = j['price']['currencyCode']
                new_price_return.price_USD = float(new_price_return.price) / currency_json['rates'][new_price_return.currency]
            new_price_return.price_type = priceType
            new_price_return.update_date = timezone.now()
            airport_d_return = Airport.objects.get(iata_code=j['departureStation'])
            airport_a_return = Airport.objects.get(iata_code=j['arrivalStation'])
            new_price_return.departureStation = airport_d_return.name  # j['departureStation']
            new_price_return.arrivalStation = airport_a_return.name  # j['arrivalStation']
            new_price_return.air_company = 'WiZZ Air'
            new_price_return.save()

        request_res.update(request_1)

    return render(request, 'wizz/search_form.html', {
        'form': form,
        'request_res': request_res
})

def wizz(request):
    # request to wizzair website
    # request_url = "https://be.wizzair.com/7.5.2/Api/search/timetable"
    # head = {'content-type': 'application/json'}
    # payload = {"flightList":[{"departureStation":"IEV","arrivalStation":"BUD","from":"2017-11-20","to":"2017-12-03"},{"departureStation":"BUD","arrivalStation":"IEV","from":"2017-11-27","to":"2017-12-31"}],"priceType":"regular"}
    # req = requests.post(request_url, headers=head, data=json.dumps(payload))
    # req_content1 = req.content

    data = {"outboundFlights":[{"departureStation":"IEV","arrivalStation":"BUD","departureDate":"2017-11-20T00:00:00","price":{"amount":2619.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-11-20T07:10:00"],"classOfService":"J","hasMacFlight":False},{"departureStation":"IEV","arrivalStation":"BUD","departureDate":"2017-11-22T00:00:00","price":{"amount":1889.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-11-22T07:10:00"],"classOfService":"KL","hasMacFlight":False},{"departureStation":"IEV","arrivalStation":"BUD","departureDate":"2017-11-24T00:00:00","price":{"amount":1599.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-11-24T07:10:00"],"classOfService":"LB","hasMacFlight":False},{"departureStation":"IEV","arrivalStation":"BUD","departureDate":"2017-11-25T00:00:00","price":{"amount":1449.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-11-25T07:10:00"],"classOfService":"B","hasMacFlight":False},{"departureStation":"IEV","arrivalStation":"BUD","departureDate":"2017-11-26T00:00:00","price":{"amount":1449.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-11-26T07:10:00"],"classOfService":"B","hasMacFlight":False},{"departureStation":"IEV","arrivalStation":"BUD","departureDate":"2017-11-27T00:00:00","price":{"amount":2319.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-11-27T07:10:00"],"classOfService":"JK","hasMacFlight":False},{"departureStation":"IEV","arrivalStation":"BUD","departureDate":"2017-11-29T00:00:00","price":{"amount":2909.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-11-29T07:10:00"],"classOfService":"IJ","hasMacFlight":False},{"departureStation":"IEV","arrivalStation":"BUD","departureDate":"2017-12-01T00:00:00","price":{"amount":1749.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-01T07:10:00"],"classOfService":"L","hasMacFlight":False},{"departureStation":"IEV","arrivalStation":"BUD","departureDate":"2017-12-02T00:00:00","price":{"amount":1449.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-02T07:10:00"],"classOfService":"B","hasMacFlight":False},{"departureStation":"IEV","arrivalStation":"BUD","departureDate":"2017-12-03T00:00:00","price":{"amount":2039.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-03T07:10:00"],"classOfService":"K","hasMacFlight":False}],"returnFlights":[{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-11-27T00:00:00","price":{"amount":1889.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-11-27T08:20:00"],"classOfService":"KL","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-11-29T00:00:00","price":{"amount":1749.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-11-29T08:20:00"],"classOfService":"L","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-01T00:00:00","price":{"amount":999.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-01T08:20:00"],"classOfService":"OP","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-02T00:00:00","price":{"amount":1749.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-02T08:20:00"],"classOfService":"L","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-03T00:00:00","price":{"amount":1599.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-03T08:20:00"],"classOfService":"LB","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-04T00:00:00","price":{"amount":2039.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-04T08:20:00"],"classOfService":"K","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-06T00:00:00","price":{"amount":2619.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-06T08:20:00"],"classOfService":"J","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-07T00:00:00","price":{"amount":1599.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-07T08:20:00"],"classOfService":"LB","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-08T00:00:00","price":{"amount":799.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-08T08:20:00"],"classOfService":"PR","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-09T00:00:00","price":{"amount":1149.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-09T08:20:00"],"classOfService":"O","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-10T00:00:00","price":{"amount":1749.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-10T08:20:00"],"classOfService":"L","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-11T00:00:00","price":{"amount":1599.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-11T08:20:00"],"classOfService":"LB","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-12T00:00:00","price":{"amount":1449.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-12T08:20:00"],"classOfService":"B","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-13T00:00:00","price":{"amount":1149.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-13T08:20:00"],"classOfService":"O","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-15T00:00:00","price":{"amount":1149.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-15T08:20:00"],"classOfService":"O","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-16T00:00:00","price":{"amount":1149.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-16T08:20:00"],"classOfService":"O","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-17T00:00:00","price":{"amount":2039.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-17T08:20:00"],"classOfService":"K","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-18T00:00:00","price":{"amount":1889.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-18T08:20:00"],"classOfService":"KL","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-19T00:00:00","price":{"amount":1599.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-19T08:20:00"],"classOfService":"LB","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-20T00:00:00","price":{"amount":1889.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-20T08:20:00"],"classOfService":"KL","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-21T00:00:00","price":{"amount":2039.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-21T08:20:00"],"classOfService":"K","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-22T00:00:00","price":{"amount":1749.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-22T08:20:00"],"classOfService":"L","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-23T00:00:00","price":{"amount":1889.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-23T08:20:00"],"classOfService":"KL","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-24T00:00:00","price":{"amount":1889.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-24T08:20:00"],"classOfService":"KL","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-26T00:00:00","price":{"amount":2319.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-26T08:20:00"],"classOfService":"JK","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-27T00:00:00","price":{"amount":2619.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-27T08:20:00"],"classOfService":"J","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-28T00:00:00","price":{"amount":1889.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-28T08:20:00"],"classOfService":"KL","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-29T00:00:00","price":{"amount":1889.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-29T08:20:00"],"classOfService":"KL","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-30T00:00:00","price":{"amount":1749.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-30T08:20:00"],"classOfService":"L","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-31T00:00:00","price":{"amount":1599.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-31T08:20:00"],"classOfService":"LB","hasMacFlight":False}]}

    dict1 = json.dumps(data)
    req_content = json.loads(dict1)
    return render(request, 'wizz/results.html', {
        'req_content': req_content,
        })
