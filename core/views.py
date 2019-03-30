from django.shortcuts import render
from github import Github,GithubException
from django.conf import settings
from .forms import DictionaryForm
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
        'isp':geodata['isp'],
        'region':geodata['regionName'],
        'longitude':geodata['lon'],
        'api_key':settings.GOOGLE_MAPS_API_KEY,
        'is_cached': is_cached
    })

def github(request):
    search_result = {}
    if 'username' in request.GET:
        username = request.GET['username']
        url = 'https://api.github.com/users/%s' % username
        response = requests.get(url)
        search_was_successful = (response.status_code == 200)
        search_result = response.json()
        search_result['success'] = search_was_successful
        search_result['rate']={
            'limit':response.headers['X-RateLimit-Limit'],
            'remaining':response.headers['X-RateLimit-Remaining'],
        }
    return render(request,'github.html', {'search_result':search_result})

def github_client(request):
    search_result = {}
    if 'username' in request.GET:
        username = request.GET['username']
        client = Gihub()

        try:
            user = client.get_user(username)
            search_result['name'] = user.name
            search_result['login'] = user.login
            search_result['public_repos'] = user.public_repos
            search_result['success'] = False

        except GithubException as ge:
            search_result['message'] =ge.data['message']
            search_result['success'] = False

        rate_limit = client.get_rate_limit()
        search_result['rate'] ={
            'limit': rate_limit.rate.limit,
            'remaining': rate_limit.rate.remaining,
        }

    return render(request, 'github.html', {'search_result':search_result})

def oxford(request):
    search_result = {}
    if 'word' in request.GET:
        form = DictionaryForm(request.GET)
        if form.is_valid():
            search_result = form.search()
    else:
        form = DictionaryForm()
    return render(request, 'oxford.html', {'form':form,'search_result':search_result})
