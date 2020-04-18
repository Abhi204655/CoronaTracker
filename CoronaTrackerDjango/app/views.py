from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
import json
# Create your views here.


def home(request):
    url = "https://covid19.mathdro.id/api/daily"
    try:
        # response = requests.get(url).json()
        response = requests.get("https://covid19.mathdro.id/api/daily").json()
    except Exception:
        return HttpResponse("Some error occured!!")

    try:
        res = requests.get("https://covid19.mathdro.id/api").json()
    except Exception:
        return HttpResponse("Some error occured!!")

    try:
        countryResponse = requests.get(
            "https://covid19.mathdro.id/api/countries").json()
    except Exception:
        return HttpResponse("Some error occured!!")

    countries = []
    values = countryResponse["countries"]
    for i in values:
        countries.append(i["name"])

    confirmed = []
    deaths = []
    date = []
    for i in response:
        confirmed.append(i['confirmed']['total'])
        deaths.append(i['deaths']['total'])
        date.append(i['reportDate'])
    context = {
        "confirmedCases": res['confirmed']['value'],
        "recoveredCases": res['recovered']['value'],
        "deathCount": res['deaths']['value'],
        "lastUpdate": res['lastUpdate'][:10],
        "deaths": deaths,
        "confirmed": confirmed,
        "date": date,
        "countries": countries,
        "bar": False
    }
    return render(request, "app/index.html", context)


def countryData(request):
    if request.method == 'POST':
        country = request.POST['dropdown']
        print(country)
        if(country == 'Nothing'):
            return redirect('/')
        else:
            # url = 'https://covid19.mathdro.id/api/countries/' + country
            try:
                # response = requests.get(url).json()
                response = requests.get(
                    'https://covid19.mathdro.id/api/countries/' + country).json()
            except Exception:
                return HttpResponse("Some error occured!!")

            try:
                countryResponse = requests.get(
                    "https://covid19.mathdro.id/api/countries").json()
            except Exception:
                return HttpResponse("Some error occured!!")

            countries = []
            values = countryResponse["countries"]
            for i in values:
                countries.append(str(i["name"]))

            context = {
                # "confirmedCases": response['confirmed']['value'],
                "confirmedCases": response.get('confirmed').get('value'),

                # "recoveredCases": response['recovered']['value'],
                "recoveredCases": response.get('recovered').get('value'),

                # "deathCount": response['deaths']['value'],
                "deathCount": response.get('deaths').get('value'),

                # "lastUpdate": response['lastUpdate'][:10],
                "lastUpdate": response.get('lastUpdate')[:10],

                "countries": countries,
                "bar": True,
                "countryName": country
            }
            return render(request, 'app/index.html', context)
    else:
        return redirect('/')
