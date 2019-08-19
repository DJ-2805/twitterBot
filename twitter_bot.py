from twython import Twython, TwythonError
from pandas import read_csv
from random import randint
from PIL import Image

app_key = '9AhPSwqckmWmPMx6Q8QZy7prt'
app_secret = 'tzPHFncPr4dwvgkYJMoiTLopcFFUKYev65rAnGqt96B79No1gE'

acc_tok = '1075518467707527168-FXvV9mw6onLPNKWgBr4Ohq28ehCOST'
acc_secret = 'TGOnjrECN80kPaFc1w1euqHezMz4WckfT1N8LISTyEFSh'

csv_path = './resources/tweets.csv'
img_path = '../tweets/'

def getBlock(blocks,size):
    randi = randint(0,size-1)
    geoid = blocks['GeoID'][randi]
    text = blocks['Text'][randi]
    blocks = blocks.drop(randi)
    blocks.to_csv(csv_path)
    return text,geoid

def twitterBot(text,geoid):
    twitter = Twython(app_key, app_secret, acc_tok, acc_secret)

    photo = Image.open(img_path+geoid+'.png')
    try:
        response = twitter.upload_media(media=photo)
        twitter.update_status(status=text, media_ids=[response['media_id']])
    except TwythonError as e:
        print (e)

if __name__ == "__main__":
    data = read_csv(path)
    blocks = data[['GeoID','Text']]
    size = blocks.shape[0]

    text,geoid = getBlock(blocks,size)
    twitterBot(text,geoid)
