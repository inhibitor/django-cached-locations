# -*- coding: utf-8 -*-

from decimal import *
import json
import urllib
import urllib2
from django.conf import settings


class AddressNotFound(Exception):
    """Address was not found by reasons:
        - google maps was not available or they changes API
        - address format is incorrect
        - service returns an error
    """
    
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)


def gm_get_coordinates(address):
    """Returns geo coordinates by location address"""
    address = urllib.quote_plus(address)
    request = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % address
    data = json.loads(urllib.urlopen(request).read())

    if data['status'] == 'OK':
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        return Decimal(lat), Decimal(lng)
    else:
        raise AddressNotFound('Address %s was not found' % address)


def gm_get_location(latitude, longitude):
    """
    Returns location address by geo coordinates.
    Google limitations: 2500 requests per day
    """
    headers = {
        'Accept-Language': settings.LANGUAGE_CODE,
    }

    url = "http://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&sensor=false" % \
          (str(latitude), str(longitude))
    req = urllib2.Request(url, None, headers)
    opener = urllib2.build_opener()
    response = opener.open(req).read()
    data = json.loads(response)
    space = " "

    if data['status'] == 'OK':
        result = {}
        results = data['results']
        if len(results):
            most_prominent = results[0]['address_components']

            # geo keys
            keys_scheme = {'town': 'locality', 'street': 'route', 'number': 'street_number'}

            for chunk in most_prominent:
                for key in keys_scheme.keys():
                    if keys_scheme[key] in chunk['types']:
                        result[key] = chunk['short_name']

            result['street'] = space.join(result['street'].split()[1:])  # Normalize street name
        return result
    else:
        raise AddressNotFound('Location (%s, %s) was not found' % (str(latitude), str(longitude)))


# Simple tests
def main():
    print(gm_get_coordinates("Россия, Ставрополь, 1-ая Промышленная 3а"))
    print(gm_get_location(Decimal(45.009209), Decimal(41.924027)))


if __name__ == '__main__':
    main()
