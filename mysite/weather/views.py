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
    matt = response.json()
    print ("\n \n")

    users_data=[]

    for i in matt:
        print('uuid  : ' + i['uuid'])
        print('applicationUuid : ' + i['applicationUuid'])
        print ('applicationUserId : '+ i['applicationUserId'])
        print('referenceId : ' + i['referenceId'])
        print('institutionConsents : ' + i['institutionConsents'][0]['institutionId'])
        print("\n \n")
        banking_user = {
            'uuid' : i['uuid'],
            'applicationUuid' : i['applicationUuid'],
            'applicationUserId' : i['applicationUserId'],
            'referenceId': i['referenceId'],
            'institutionConsents':  i['institutionConsents'][0]['institutionId'],

        }
        users_data.append(banking_user)

    print(users_data)
    print(response.json())

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

    context = {'users_data' : users_data,'weather_data' : weather_data, 'form' : form}
    return render(request, 'weather/weather.html', context)