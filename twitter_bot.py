import requests # an http library written for humans
from twython import Twython, TwythonError
import time

# ref source 2 if comments are unclear for this section
apiKey = key # your unique api key in the field
apiUrl = url # https://the url in the field

# ref source 3
appKey = 'Your Key'
appSecret = 'Your Secret Key'
oauthToken = 'Your token'
oauthTokenSecret = 'Your secret Token'

twitter = Twython(appKey, appSecret, oauthToken, oauthTokenSecret)

# liners.txt will be replaced with geo data
# NOTE: look into getting images
# NOTE: see how geo data determines the image selected
# possible API's that can help with geo data and sat images
try:
    with open('liners.txt', 'r+') as tweetfile:
		buff = tweetfile.readlines()

    for line in buff[:]:
		line = line.strip(r'\n') #Strips any empty line.
		if len(line)<=140 and len(line)>0:
			print ("Tweeting...")
			twitter.update_status(status=line)
			with open ('liners.txt', 'w') as tweetfile:
				buff.remove(line) #Removes the tweeted line.
				tweetfile.writelines(buff)
			time.sleep(900)
		else:
			with open ('liners.txt', 'w') as tweetfile:
				buff.remove(line) #Removes the line that has more than 140 characters.
				tweetfile.writelines(buff)
			print ("Skipped line - Char length violation")
			continue
    print ("No more lines to tweet...") #When you see this... Well :) Go find some new tweets...

except TwythonError as e:
	print (e)
