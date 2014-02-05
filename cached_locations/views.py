import json
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from cached_locations.api import get_address_by_coordinates


@cache_page(60 * 15)
def get_formatted_address(request):
    latitude = request.GET.get('lat', 0)
    longitude = request.GET.get('lon', 0)

    response = {'status': 404, 'address': ''}
    address = get_address_by_coordinates(latitude, longitude)
    if not address is None:
        response['status'] = 200
        response['address'] = unicode(address)

    return HttpResponse(json.dumps(response), 'application/json')
