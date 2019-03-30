from django.shortcuts import render
import requests 

def home(request):
    response = requests.get('http://ip-api.com/json/')
    geodata = response.json()
    return render (request, 'home.html', {'ip':geodata['query'],'country':geodata['country']})
