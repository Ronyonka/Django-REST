from django.shortcuts import render
from django.conf import settings
import requests 

def home(request):
    response = requests.get('http://ip-api.com/json/')
    geodata = response.json()
    return render (request, 'home.html', {
        'ip':geodata['query'],
        'isp':geodata['isp'],
        'country':geodata['country'],
        'latitude':geodata['lat'],
        'longitude':geodata['lon'],
        'api_key':settings.GOOGLE_MAPS_API_KEY,
    })

