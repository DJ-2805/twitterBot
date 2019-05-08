import pandas as pd
import screenshot as ss
from random import randint

# name of the csv file
name = '037latlon.csv'

# reading csv file into file
blocks = pd.read_csv(name)

# extracting necessary columns
latlon = blocks[['INTPTLAT10','INTPTLON10']]
# getting current length amount
length = latlon.shape[0]
# generating random int within the size of the array
randi = randint(0,length-1)

# random int selects a certain block within LA county
lat = latlon['INTPTLAT10'][randi]
lon = latlon['INTPTLON10'][randi]
# generates jpg of chosen block
ss.main(lat,lon)

# drops the used row and loads csv for future use
# latlon = latlon.drop(randi)
# latlon.to_csv(name)
