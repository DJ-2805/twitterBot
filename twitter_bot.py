from twython import Twython, TwythonError

app_key = '9AhPSwqckmWmPMx6Q8QZy7prt'
app_secret = 'tzPHFncPr4dwvgkYJMoiTLopcFFUKYev65rAnGqt96B79No1gE'

acc_tok = '1075518467707527168-FXvV9mw6onLPNKWgBr4Ohq28ehCOST'
acc_secret = 'TGOnjrECN80kPaFc1w1euqHezMz4WckfT1N8LISTyEFSh'

twitter = Twython(app_key, app_secret, acc_tok, acc_secret)

# attachment_url: to website for reference to block
# media_ids: jpg?
# status: information about block
# NOTE: status must be unique, so that Twitter doesn't block the tweet
try:
    twitter.update_status(status='Hello World!')
except TwythonError as e:
    print (e)