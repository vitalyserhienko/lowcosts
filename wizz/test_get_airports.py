from .models import Airport
import requests
import json

def get_wizzair_airports(request, city_code):
    ap_request = requests.get('https://be.wizzair.com/7.7.1/Api/asset/map?languageCode=uk-ua')
    req_json = json.loads(ap_request.content)

    kiev_connections = []

    for city in req_json['cities']:
        if city['iata'] == "IEV":
            for connect in city['connections']:
                kiev_connections.append(connect['iata'])

    for city in req_json['cities']:
        for ap in kiev_connections:
            if ap == city['iata']:
                # print(str(city['countryName']) + " // " + str(city['shortName']) + " // " + str(city['iata']) + " // " + str(city['longitude']) + " // " + str(city['latitude']))
                airport, created = Airport.objects.get_or_create(iata_code=city['iata'])
                if created:
                    new_airport = Airport()
                    new_airport.name = city['shortName'] + " (" + city['iata'] + ")"
                    new_airport.counrty = city['countryName']
                    new_airport.city = city['shortName']
                    new_airport.iata_code = city['iata']
                    new_airport.longitude = city['longitude']
                    new_airport.latitude = city['latitude']
                    new_airport.save()

                else:
                    print("Already have this airport")



            # print(city['shortName'])
    # if city['iata'] == 'IEV':
    #     print(city['iata']['connections'])
# print(kiev_connections)

    # return req_json