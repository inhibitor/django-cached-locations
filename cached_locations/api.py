from models import Town, Street, Address
from cached_locations.maps import gm_get_location
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist


def get_address_by_coordinates(latitude, longitude):
    """Returns address object by coordinates"""
    try:
        address = Address.objects.get(latitude=Decimal(latitude), longitude=Decimal(longitude))
    except ObjectDoesNotExist:

        try:
            address_chunks = gm_get_location(Decimal(latitude), Decimal(longitude))
        except:
            return None

        town, created = Town.objects.get_or_create(name=address_chunks['town'])
        street, created = Street.objects.get_or_create(name=address_chunks['street'], town=town)

        street_number = address_chunks['number']
        address = Address(street=street, street_number=street_number)
        address.save()
    else:
        return None

    return address
