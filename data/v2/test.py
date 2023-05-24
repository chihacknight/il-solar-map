import requests

r = requests.get(
    "https://geocoding.geo.census.gov/geocoder/geographies/coordinates?benchmark=4&format=json&vintage=4&x=-89.0276159&y=42.3557634")


jsonVal = r.json()

print(jsonVal["result"]["geographies"]["Census Tracts"][0]["GEOID"])
