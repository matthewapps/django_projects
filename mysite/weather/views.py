import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm


def index(request):
    url = "https://api.yapily.com/users"

    payload = {}
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': 'Basic NjgzODYxNzgtZDUwZi00ZjVjLTgwMDEtMjY1ZDViZjAwMmNjOmI1NGQ3MjJmLWZkN2MtNDM3MS1iODE3LWIwYzMyMjU0MDdhYw=='
    }

    response = requests.request("GET", url, headers=headers, data = payload)

    print(response.text.encode('utf8'))

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=16425e59cea49695c57071000f04e977'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {'weather_data' : weather_data, 'form' : form}
    return render(request, 'weather/weather.html', context)