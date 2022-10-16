from django.db import models

class Country(models.Model):
    name         = models.CharField(max_length = 20)

    class Meta:
        db_table = "countries"

class Region(models.Model):
    name        = models.CharField(max_length = 20)
    country     = models.ForeignKey("Country", on_delete = models.CASCADE)

    class Meta:
        db_table = "regions"



