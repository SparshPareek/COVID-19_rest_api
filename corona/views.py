from django.shortcuts import render, redirect
from rest_framework import generics
from .models import CountryData
from .serializers import CountryDataSerializer
from .pagination import LargeResultSetPagination
from bs4 import BeautifulSoup
import requests
# Create your views here.

from django.http import HttpResponse
import requests

def find(key, dictionary):
    for k, v in dictionary.items():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in find(key, d):
                    yield result

def home(request):
	response = requests.get('https://thevirustracker.com/free-api?countryTotal=IN', headers={'User-Agent' : 'PostmanRuntime/7.24.0'})

	total_cases = list(find('total_cases', response.json()))[0]
	print("total_cases: {}".format(total_cases))
	total_recovered = list(find('total_recovered', response.json()))[0]
	total_deaths = list(find('total_deaths', response.json()))[0]
	total_new_cases_today = list(find('total_new_cases_today', response.json()))[0]
	return render(request, 'home.html', {'total_cases': total_cases, 
		'total_recovered': total_recovered,
		'total_deaths': total_deaths,
		'total_new_cases_today': total_new_cases_today})

def scrape(request):
	response = requests.get("https://www.worldometers.info/coronavirus/")

	bs = BeautifulSoup(response.text)

	table = bs.find(id="main_table_countries_today")

	# header_list = []
	# for i in table.find("tr").find_all("th"):
	#     header_list.append(i.get_text().split(",")[0].replace(" ", ""))

	for i in table.find_all("tr")[1:]:
	    row_data = []
	    for j in i.find_all("td")[:-2]:
	        row_data.append(j.text.strip())
	    country_data = CountryData()
	    country_data.Country = row_data[0]
	    country_data.TotalCases = row_data[1]
	    country_data.NewCases = row_data[2]
	    country_data.TotalDeaths = row_data[3]
	    country_data.NewDeaths = row_data[4]
	    country_data.TotalRecovered = row_data[5]
	    country_data.ActiveCases = row_data[6]
	    country_data.Serious = row_data[7]
	    country_data.save()

	return redirect("cases")


class ListCountryCases(generics.ListAPIView):
	queryset = CountryData.objects.all()
	serializer_class = CountryDataSerializer
	pagination_class = LargeResultSetPagination

	def get_queryset(self):
		queryset = CountryData.objects.all()
		country = self.request.query_params.get('country', None)
		if country is not None:
			return CountryData.objects.filter(Country=country)
		return queryset