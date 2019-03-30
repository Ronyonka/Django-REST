from django.shortcuts import render
from django.conf import settings
import requests 

def home(request):
    is_cached = ('geodata' in request.session)

    if not is_cached:
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '')
        response = requests.get('http://ip-api.com/json/')
        request.session['geodata'] = response.json()
    geodata = request.session['geodata']
    return render (request, 'home.html', {
        'ip':geodata['query'],
        'isp':geodata['isp'],
        'country':geodata['country'],
        'latitude':geodata['lat'],
        'longitude':geodata['lon'],
        'api_key':settings.GOOGLE_MAPS_API_KEY,
        'is_cached': is_cached
    })

def github(request):
    user = {}
    if 'username' in request.GET:
        username = request.GET['username']
        url = 'https://api.github.com/users/%s' % username
        response = requests.get(url)
        user = response.json()
    return render(request,'github.html', {'user':user})
