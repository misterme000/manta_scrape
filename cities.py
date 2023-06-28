
from pandas import *
from geosky import geo_plug
import pandas as pd
df = pd.read_csv('states - states.csv')
# print(df)
data = read_csv("states - states.csv")


stateList = data['state'].tolist()
cities = geo_plug.all_State_CityNames(stateList[5]) # .tolist()
print(cities)
print(stateList[5])
# 

# countries = geo_plug.all_CountryNames()

# geo_plug.all_Country_StateNames()

# cities = geo_plug.all_State_CityNames('all')  # name == 'all' or stae name
# #geo_plug.all_State_CityNames('Odisha')
# print(cities)
# print(countries)






#states[] = list(pd.read_csv('states - states.csv', usecols=['state']))
#print(pd.read_csv('states - states.csv', usecols=['state']))
