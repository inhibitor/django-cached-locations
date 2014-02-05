django-cached-locations
=======================

Abstract django example app

###Version: 0.01

features:
------
* Returns full formatted address by geo coordinates (latitude and longitude)
* Gets address and save it in db
* Caching results in views (returns json response with formatted address)

Usage:
------
1. Add 'cached_locations' line in INSTALLED_APPS
2. Use get_address_by_coordinates(latitude, longitude) from cached_locations.api module
3. Use get_formatted_address(request) with Get params: 'lat', 'lon' in your own views
