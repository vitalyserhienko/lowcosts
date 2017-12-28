from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from .models import Airport, priceType, priceTemplate, Price
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import FlightSearchForm
from .wizz_request import request_data
from .new_request_number import new_request_number
from .dates_from_range import get_dates_range
from django.utils import timezone
import requests
import json
from time import sleep

# Create your views here.
def home(request):
    return render(request, 'base.html', {})

def search_history(request):
    prices = Price.objects.all().order_by('price_USD', 'update_date')
    paginator = Paginator(prices, 50)
    page = request.GET.get('page')
    try:
        prices = paginator.page(page)
    except PageNotAnInteger:
        prices = paginator.page(1)
    except EmptyPage:
        prices = paginator.page(paginator.num_pages)
    # contacts = paginator.get_page(page)
    return render(request, 'wizz/history.html', { 'prices': prices })

def get_search_results(request, request_id):
    prices = Price.objects.filter(request_id=request_id).order_by('price_USD', 'update_date')
    return render(request, 'wizz/results.html', {'prices': prices})

def get_all_requests(request):
    requests = Price.objects.order_by().values('request_id').distinct()
    print(requests)
    return render(request, 'wizz/all_requests.html', {'requests': requests})

def flight_search_form(request):
    form = FlightSearchForm(request.POST)
    if request.method == 'POST':
        request_id = new_request_number()
        departureStation = request.POST.get('departureStation')
        arrivalStation = request.POST.get('arrivalStation')
        dateFrom = request.POST.get('date_from')
        dateTo = request.POST.get('date_to')
        priceType = request.POST.get('priceType')

        dates_range = get_dates_range(dateFrom, dateTo)
        request_index = 0
        while request_index < len(dates_range['dates_from']):
            date_from = dates_range['dates_from'][request_index]
            date_to = dates_range['dates_to'][request_index]

            request_1 = request_data(departureStation, arrivalStation, date_from, date_to, priceType)
            currency_now = requests.get('https://openexchangerates.org/api/latest.json?app_id=6cdf29a6391b479cb9d0a4fe9608fa04')
            currency_json = json.loads(currency_now.content)
            for j in request_1['outboundFlights']:
                new_price = Price()
                new_price.request_id = request_id
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
                new_price_return.request_id = request_id
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

            request_index += 1
            sleep(5)
        # request_res.update(request_1)
        url = reverse('search-results', kwargs={'request_id': request_id})
        return HttpResponseRedirect(url)
    return render(request, 'wizz/search_form.html', {'form': form})

def get_wizzair_airports(request, city_code):
    ap_request = requests.get('https://be.wizzair.com/7.7.1/Api/asset/map?languageCode=uk-ua')
    req_json = json.loads(ap_request.content)
    kiev_connections = []
    for city in req_json['cities']:
        if city['iata'] == city_code:
            airport = Airport.objects.get_or_create(
                iata_code=city['iata'],
                name=city['shortName'] + " (" + city['iata'] + ")",
                counrty=city['countryName'],
                city=city['shortName'],
                longitude=city['longitude'],
                latitude=city['latitude'],
            )
            for connect in city['connections']:
                kiev_connections.append(connect['iata'])
    for city in req_json['cities']:
        for ap in kiev_connections:
            if ap == city['iata']:
                airport = Airport.objects.get_or_create(
                iata_code=city['iata'],
                name=city['shortName'] + " (" + city['iata'] + ")",
                counrty=city['countryName'],
                city=city['shortName'],
                longitude=city['longitude'],
                latitude=city['latitude'],
            )
    return HttpResponse("Done")

# def wizz(request):
#     # request to wizzair website
#     # request_url = "https://be.wizzair.com/7.5.2/Api/search/timetable"
#     # head = {'content-type': 'application/json'}
#     # payload = {"flightList":[{"departureStation":"IEV","arrivalStation":"BUD","from":"2017-11-20","to":"2017-12-03"},{"departureStation":"BUD","arrivalStation":"IEV","from":"2017-11-27","to":"2017-12-31"}],"priceType":"regular"}
#     # req = requests.post(request_url, headers=head, data=json.dumps(payload))
#     # req_content1 = req.content
#
#     data = {"outboundFlights":[{"departureStation":"IEV","arrivalStation":"BUD","departureDate":"2017-11-20T00:00:00","price":{"amount":2619.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-11-20T07:10:00"],"classOfService":"J","hasMacFlight":False},{"departureStation":"IEV","arrivalStation":"BUD","departureDate":"2017-11-22T00:00:00","price":{"amount":1889.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-11-22T07:10:00"],"classOfService":"KL","hasMacFlight":False},{"departureStation":"IEV","arrivalStation":"BUD","departureDate":"2017-11-24T00:00:00","price":{"amount":1599.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-11-24T07:10:00"],"classOfService":"LB","hasMacFlight":False},{"departureStation":"IEV","arrivalStation":"BUD","departureDate":"2017-11-25T00:00:00","price":{"amount":1449.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-11-25T07:10:00"],"classOfService":"B","hasMacFlight":False},{"departureStation":"IEV","arrivalStation":"BUD","departureDate":"2017-11-26T00:00:00","price":{"amount":1449.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-11-26T07:10:00"],"classOfService":"B","hasMacFlight":False},{"departureStation":"IEV","arrivalStation":"BUD","departureDate":"2017-11-27T00:00:00","price":{"amount":2319.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-11-27T07:10:00"],"classOfService":"JK","hasMacFlight":False},{"departureStation":"IEV","arrivalStation":"BUD","departureDate":"2017-11-29T00:00:00","price":{"amount":2909.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-11-29T07:10:00"],"classOfService":"IJ","hasMacFlight":False},{"departureStation":"IEV","arrivalStation":"BUD","departureDate":"2017-12-01T00:00:00","price":{"amount":1749.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-01T07:10:00"],"classOfService":"L","hasMacFlight":False},{"departureStation":"IEV","arrivalStation":"BUD","departureDate":"2017-12-02T00:00:00","price":{"amount":1449.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-02T07:10:00"],"classOfService":"B","hasMacFlight":False},{"departureStation":"IEV","arrivalStation":"BUD","departureDate":"2017-12-03T00:00:00","price":{"amount":2039.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-03T07:10:00"],"classOfService":"K","hasMacFlight":False}],"returnFlights":[{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-11-27T00:00:00","price":{"amount":1889.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-11-27T08:20:00"],"classOfService":"KL","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-11-29T00:00:00","price":{"amount":1749.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-11-29T08:20:00"],"classOfService":"L","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-01T00:00:00","price":{"amount":999.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-01T08:20:00"],"classOfService":"OP","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-02T00:00:00","price":{"amount":1749.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-02T08:20:00"],"classOfService":"L","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-03T00:00:00","price":{"amount":1599.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-03T08:20:00"],"classOfService":"LB","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-04T00:00:00","price":{"amount":2039.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-04T08:20:00"],"classOfService":"K","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-06T00:00:00","price":{"amount":2619.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-06T08:20:00"],"classOfService":"J","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-07T00:00:00","price":{"amount":1599.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-07T08:20:00"],"classOfService":"LB","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-08T00:00:00","price":{"amount":799.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-08T08:20:00"],"classOfService":"PR","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-09T00:00:00","price":{"amount":1149.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-09T08:20:00"],"classOfService":"O","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-10T00:00:00","price":{"amount":1749.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-10T08:20:00"],"classOfService":"L","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-11T00:00:00","price":{"amount":1599.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-11T08:20:00"],"classOfService":"LB","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-12T00:00:00","price":{"amount":1449.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-12T08:20:00"],"classOfService":"B","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-13T00:00:00","price":{"amount":1149.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-13T08:20:00"],"classOfService":"O","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-15T00:00:00","price":{"amount":1149.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-15T08:20:00"],"classOfService":"O","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-16T00:00:00","price":{"amount":1149.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-16T08:20:00"],"classOfService":"O","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-17T00:00:00","price":{"amount":2039.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-17T08:20:00"],"classOfService":"K","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-18T00:00:00","price":{"amount":1889.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-18T08:20:00"],"classOfService":"KL","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-19T00:00:00","price":{"amount":1599.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-19T08:20:00"],"classOfService":"LB","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-20T00:00:00","price":{"amount":1889.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-20T08:20:00"],"classOfService":"KL","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-21T00:00:00","price":{"amount":2039.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-21T08:20:00"],"classOfService":"K","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-22T00:00:00","price":{"amount":1749.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-22T08:20:00"],"classOfService":"L","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-23T00:00:00","price":{"amount":1889.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-23T08:20:00"],"classOfService":"KL","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-24T00:00:00","price":{"amount":1889.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-24T08:20:00"],"classOfService":"KL","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-26T00:00:00","price":{"amount":2319.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-26T08:20:00"],"classOfService":"JK","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-27T00:00:00","price":{"amount":2619.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-27T08:20:00"],"classOfService":"J","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-28T00:00:00","price":{"amount":1889.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-28T08:20:00"],"classOfService":"KL","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-29T00:00:00","price":{"amount":1889.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-29T08:20:00"],"classOfService":"KL","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-30T00:00:00","price":{"amount":1749.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-30T08:20:00"],"classOfService":"L","hasMacFlight":False},{"departureStation":"BUD","arrivalStation":"IEV","departureDate":"2017-12-31T00:00:00","price":{"amount":1599.00,"currencyCode":"UAH"},"priceType":"price","departureDates":["2017-12-31T08:20:00"],"classOfService":"LB","hasMacFlight":False}]}
#
#     dict1 = json.dumps(data)
#     req_content = json.loads(dict1)
#     return render(request, 'wizz/results.html', {
#         'req_content': req_content,
#         })
