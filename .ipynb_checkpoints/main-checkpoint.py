import pandas as pd
import revisionGrab as rg
from random import randint

# name of the csv file
name = 'resources/zoomValues.csv'

# reading csv file into file
data = pd.read_csv(name)

# extracting necessary columns
blocks = data[['GeoID','Link']]
size = blocks.shape[0] # 10133

rg.grabBlockImage(blocks,size)
rg.clipBlockImage(blocks,size)
