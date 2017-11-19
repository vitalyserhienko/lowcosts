from django.shortcuts import render
from .models import Airport, priceType, priceTemplate
import requests
import json

# Create your views here.
def home(request):
    return render(request, 'wizz/index.html', {})

def wizz(request):
    request_url = "https://be.wizzair.com/7.5.2/Api/search/timetable"
    head = {'content-type': 'application/json'}
    payload = {"flightList":[{"departureStation":"IEV","arrivalStation":"BUD","from":"2017-11-20","to":"2017-12-03"},{"departureStation":"BUD","arrivalStation":"IEV","from":"2017-11-27","to":"2017-12-31"}],"priceType":"regular"}
    req = requests.post(request_url, headers=head, data=json.dumps(payload))
    req_content1 = req.content
    req_content = json.loads(req_content1)
    return render(request, 'wizz/index.html', {
        'req_content': req_content,
        })
