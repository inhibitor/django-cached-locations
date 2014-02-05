from django.db import models
from maps import AddressNotFound, gm_get_coordinates
from decimal import *


class Town(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Street(models.Model):
    town = models.ForeignKey(Town)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return "%s, %s" % (self.town.name, self.name)


class Address(models.Model):
    street = models.ForeignKey(Street)
    street_number = models.CharField(max_length=10)

    latitude = models.DecimalField(max_digits=11, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=6, blank=True, null=True)

    def __unicode__(self):
        return "%s, %s %s" % (self.street.town.name, self.street.name, self.street_number)

    def save(self, *args, **kwargs):
        formatted_address = "%s, %s %s" % (self.street.town.name, self.street.name, self.street_number)

        try:
            self.latitude, self.longitude = gm_get_coordinates(formatted_address.encode('utf-8'))
        except AddressNotFound:
            self.latitude, self.longitude = (Decimal(0), Decimal(0))

        super(Address, self).save(*args, **kwargs)
