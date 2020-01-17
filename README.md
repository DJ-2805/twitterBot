# twitterBot
Simple Twitter Bot to post images 

# Start Up
1. Start up the virtual environment
python3 -m venv environment
2. active the environment
source environment/bin/active
Note: should see (environment) in your terminal now
3. install your needed dependencies
pip install -r requirements.txt
# AWS commands
1. zip -g twitter.zip twitter_bot.py
2. aws lambda update-function-code --function-name its-twitter-bot --zip-file fileb://twitter.zip
