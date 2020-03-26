from django.db import models

# Create your models here.


class CountryData(models.Model):
	"""docstring for India"models.Model"""
	Country = models.CharField(max_length=255, null=False)
	TotalCases = models.CharField(max_length=255, null=False)
	NewCases = models.CharField(max_length=255, null=False)
	TotalDeaths = models.CharField(max_length=255, null=False)
	NewDeaths = models.CharField(max_length=255, null=False)
	TotalRecovered = models.CharField(max_length=255, null=False)
	ActiveCases = models.CharField(max_length=255, null=False)
	Serious = models.CharField(max_length=255, null=False)

	def __str__(self):
		return "{} - {}".format(self.TotalCases, self.ActiveCases)