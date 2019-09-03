from twython import Twython, TwythonError
from pandas import read_csv
from PIL import Image
import boto3 as b3

app_key = '9AhPSwqckmWmPMx6Q8QZy7prt'
app_secret = 'tzPHFncPr4dwvgkYJMoiTLopcFFUKYev65rAnGqt96B79No1gE'

acc_tok = '1075518467707527168-FXvV9mw6onLPNKWgBr4Ohq28ehCOST'
acc_secret = 'TGOnjrECN80kPaFc1w1euqHezMz4WckfT1N8LISTyEFSh'

s3 = b3.client('s3')
BUCKET = 'revision-geoid-images'
DATA = 'tweets.csv'
KEY = 'tweets/'
IMG_PATH = '/tmp/local.png'
CSV_PATH = '/tmp/tweets.csv'

def getBlock(blocks):
    geoid = blocks['GeoID'][0]
    text = blocks['Text'][0]
    blocks = blocks.drop(0)
    # check path
    blocks.to_csv(CSV_PATH)
    return text,geoid

def twitterBot(text):
    twitter = Twython(app_key, app_secret, acc_tok, acc_secret)

    photo = Image.open(IMG_PATH)

    try:
        response = twitter.upload_media(media=photo)
        twitter.update_status(status=text, media_ids=[response['media_id']])
    except TwythonError as e:
        print (e)

def lambda_handler(event,context):
    s3.download_file(BUCKET,DATA,CSV_PATH)
    soCal = read_csv(CSV_PATH)
    blocks = soCal[['GeoID','Text']]

    text,geoid = getBlock(blocks)
    s3.upload_file(CSV_PATH,BUCKET,DATA)
    s3.download_file(BUCKET,KEY+geoid+'.png',IMG_PATH)
    twitterBot(text)
