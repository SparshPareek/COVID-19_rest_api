from rest_framework import serializers
from .models import CountryData

class CountryDataSerializer(serializers.ModelSerializer):
	class Meta:
		model = CountryData
		fields = ("Country", "TotalCases", "NewCases", "TotalDeaths", "NewDeaths", "TotalRecovered", "ActiveCases", "Serious")