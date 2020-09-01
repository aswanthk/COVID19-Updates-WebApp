from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests

def home(request):
    return render(request, 'status/status-home.html')

def cases(request):
    country = request.GET['country-name']
    print(country)
    covid19_cases = covid19_data(country)
    if isinstance(covid19_cases, HttpResponse):
        return HttpResponse('<body bgcolor="#9ab3e5"><p style="font: bold 23px cursive">Oops, Check your internet connections!</p></body>')
    if isinstance(covid19_cases, str):
        return render(request, 'status/status-cases-nocountry.html', {'no_country': covid19_cases})
    return render(request, 'status/status-cases.html', covid19_cases)

def cases_india(request):
    covid19_cases = covid19_data('india')
    if isinstance(covid19_cases, HttpResponse):
        return HttpResponse('<body bgcolor="#9ab3e5"><p style="font: bold 23px cursive">Oops, Check your internet connections!</p></body>')
    if isinstance(covid19_cases, str):
        return render(request, 'status/status-cases-nocountry.html', {'no_country': "Something went wrong!"})
    return render(request, 'status/status-cases.html', covid19_cases)

def cases_world(request):
    covid19_cases = covid19_data_world('world')
    if isinstance(covid19_cases, HttpResponse):
        return HttpResponse('<body bgcolor="#9ab3e5"><p style="font: bold 23px cursive">Oops, Check your internet connections!</p></body>')
    if isinstance(covid19_cases, str):
        return render(request, 'status/status-cases-nocountry.html', {'no_country': covid19_cases})
    return render(request, 'status/status-cases.html', covid19_cases)

# FUNCTION FOR FETCH STATUS OF COUNTRYWISE COVID-19 CASES

def covid19_data(country):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    }

    country = country.strip().lower().replace(' ', '-').replace('usa', 'us')

    try:
        site = requests.get('https://www.worldometers.info/coronavirus/country/' + country, headers=headers)
    except:
        return HttpResponse('')

    if site.status_code == 200:
        soup = BeautifulSoup(site.content, 'html.parser')
        code = soup.find(class_='content-inner')

        if code:
            count = code.find_all(class_='maincounter-number')
            count_list = [num.get_text().replace('\n', '').strip() for num in count]

            count_list.append(format(int(count_list[0].replace('N/A', '0').replace(',', '')) - (int(count_list[1].replace('N/A', '0').replace(',', '')) + int(count_list[2].replace('N/A', '0').replace(',', ''))), ','))

            covid19_cases = {'covid19_cases': count_list}
            covid19_cases['country'] = country.replace('-', ' ').upper()

            return covid19_cases

        else:
            return f"Wrong entry! '{country}' is not a country"
    else:
        return "Something went wrong!"

# FUNCTION FOR FETCH STATUS OF WORLDWIDE COVID-19 CASES

def covid19_data_world(country):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    }

    country = country.upper()

    try:
        site = requests.get('https://www.worldometers.info/coronavirus/', headers=headers)
    except:
        return HttpResponse('')

    if site.status_code == 200:
        soup = BeautifulSoup(site.content, 'html.parser')
        code = soup.find_all(id='maincounter-wrap')
        count_list = []

        if len(code) == 3:
            for item in code:
                count = item.find(class_='maincounter-number')
                count_list.append(count.get_text().replace('\n', '').strip())
            count_list.append(format(int(count_list[0].replace(',', '')) - (int(count_list[1].replace(',', '')) + int(count_list[2].replace(',', ''))), ','))
            covid19_cases = {'covid19_cases': count_list}
            covid19_cases['country'] = country

            return covid19_cases

        else:
            return "Something went wrong!"
    else:
        return "Something went wrong!"
