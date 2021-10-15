

import pandas as pd
from geopy.geocoders import Nominatim


# Grab data from repo
pd_data = pd.read_csv("data/csv/SLOPD_report.csv")


def get_address_geoinfo(police_data, user_agent = "SLOPD_parser", verbose = False):

    addresses = police_data.address.str.split(';', expand = True)
    addresses.rename(columns = {0:'street_address', 1:'address_description'}, inplace = True)
    addresses.street_address = addresses.street_address.str.split('#').str[0] # remove unit numbers from address, ie 215 Chorro #15
    
    geolocator = Nominatim(user_agent="SLOPD_parser")

    location_dict = {}

    for i, address in enumerate(addresses.street_address):


            try:

                location = geolocator.geocode(f"{address}, San Luis Obispo, CA")
                location_dict[i] = {'address': location.address, 'latitude': location.latitude, 'longitude':location.longitude} 

                if verbose:
                    print(location.address)
                    print((location.latitude, location.longitude))
                    print(location.raw)

                
            except:
                
                if verbose:
                    print('No results returned. Either address not found or input address malformed or ambiguous.')

                location_dict[i] = {'address': None, 'latitude': None, 'longitude': None} 

    return location_dict

location_dict = get_address_geoinfo(police_data = pd_data.head(), user_agent = "SLOPD_parser", verbose = True)
