# ****** Twitter Bot Module *****
# AUTHOR: David James, 20190905
# Functions:
# - function getCSV
# - function getBlock
# - function getIndex
# - function writeIndex
# - function twitterBot
# - function lambda_handler
# *******************************
from twython import Twython, TwythonError
from csv import reader
from collections import OrderedDict
import boto3 as b3

# twitter access
app_key = '9AhPSwqckmWmPMx6Q8QZy7prt'
app_secret = 'tzPHFncPr4dwvgkYJMoiTLopcFFUKYev65rAnGqt96B79No1gE'
acc_tok = '1075518467707527168-FXvV9mw6onLPNKWgBr4Ohq28ehCOST'
acc_secret = 'TGOnjrECN80kPaFc1w1euqHezMz4WckfT1N8LISTyEFSh'

# s3 paths and names
s3 = b3.client('s3')
BUCKET = 'revision-geoid-images'
DATA = 'tweets.csv'
TXT = 'index.txt'
KEY = 'tweets/'

# lambda paths when uploaded
IMG_PATH = '/tmp/local.png'
CSV_PATH = '/tmp/tweets.csv'
TXT_PATH = '/tmp/index.txt'

# '''
# function getCSV
# A function designed to recover the csv and place it into
# an Ordered Dictionary
# @param: path - str, path to csv file
# @return: OrderedDict(
#          index[0] - int, geoid of block
#          index[1] - list(
#                     index[1][0] - str, text of tweet
#                     index[1][1] - int, size of tweet))
# '''
def getCSV(path):
    csvfile = open(path, mode='r')
    csvread = reader(csvfile)

    header = next(csvread)
    csvlist = []
    for row in csvread:
        csvlist.append(row)
    return csvlist

# '''
# function getBlock
# A function designed to retrieve the geoid and assoicated
# tweet for the twitter bot
# @param: blocks - OrderedDict(
#                  index[0] - int, geoid of block
#                  index[1] - list(
#                             index[1][0] - str, text of tweet
#                             index[1][1] - int, size of tweet))
#         index - int, current index of csv
# @return: text - str, tweet that twitter bot will output
#          geoid - int, geoid of block to retrieve image
# '''
def getBlock(blocks,index):
    geoid = blocks[index][0]
    text = blocks[index][1]
    return text,geoid

# '''
# function getIndex
# A function designed to retrieve the index from a text file
# @param: path - str, path to text file
# @return: index - int, current index on text file
# '''
def getIndex(path):
    file = open(path, mode='r')
    index = int(file.read())
    return index

# '''
# function writeIndex
# A function designed to write a new index to the text file
# @param: path - str, path to text file
#         index - int, current index
# @return: NONE
# '''
def writeIndex(path, index):
    file = open(path, mode='w')
    newIndex = str(index + 1)
    file.write(newIndex)

# '''
# function twitterBot
# A function meant to tweet out a status on Twitter
# @param: text - str, message to be tweeted
# @return: NONE
# '''
def twitterBot(text):
    twitter = Twython(app_key, app_secret, acc_tok, acc_secret)

    img = open(IMG_PATH,'rb')

    try:
        response = twitter.upload_media(media=img)
        twitter.update_status(status=text, media_ids=[response['media_id']])
    except TwythonError as e:
        print (e)

# '''
# function lambda_handler
# Handler function AWS uses to run previous functions
# @param: event - UNKNOWN
#         context - UNKNOWN
# @return: NONE
# '''
def lambda_handler(event,context):
    s3.download_file(BUCKET,DATA,CSV_PATH)
    s3.download_file(BUCKET,TXT,TXT_PATH)

    blist = getCSV(CSV_PATH)
    index = getIndex(TXT_PATH)
    text,geoid = getBlock(blist,index)

    writeIndex(TXT_PATH,index)

    s3.upload_file(CSV_PATH,BUCKET,DATA)
    s3.download_file(BUCKET,KEY+geoid+'.png',IMG_PATH)
    twitterBot(text)
