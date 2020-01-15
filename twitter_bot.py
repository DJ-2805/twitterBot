from twython import Twython, TwythonError
from PIL import Image
from csv import reader
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
TXT_PATH = '/tmp/index.txt'

def getCSV(path):
    csvfile = open(path, mode='r')
    csvread = reader(csvfile)
    
    header = next(csvread)
    csvlist = []
    for row in csvread:
        csvlist.append(row)
    return csvlist

def getBlock(blocks,index):
    geoid = blocks[index][0]
    text = blocks[index][1]
    return text,geoid

def getIndex(path):
    file = open(path, mode='r')
    index = int(file.read())
    return index

def writeIndex(path, index):
    file = open(path, mode='w')
    newIndex = str(index + 1)
    file.write(newIndex)

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
    
    blist = getCSV(CSV_PATH)
    index = getIndex(TXT_PATH)
    text,geoid = getBlock(blist,index)
    
    writeIndex(TXT_PATH,index)
    
    s3.upload_file(CSV_PATH,BUCKET,DATA)
    s3.download_file(BUCKET,KEY+geoid+'.png',IMG_PATH)
    twitterBot(text)
