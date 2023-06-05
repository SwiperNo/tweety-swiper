from pathlib import Path
import tweepy
import openai
import random
import os
from dotenv import load_dotenv

env_path = Path('C:\\Users\\kjon5\\repos\\tweety-swiper\\') / '.env'
load_dotenv(dotenv_path=env_path)
#load_dotenv()

# Set up Twitter API authentication

consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')

#Issue with loading Env variables using this method
#client = tweepy.Client(consumer_key,
#                       consumer_secret,
#                       access_token,
#                       access_token_secret)

#Hardcoded method - API v2 auth method
client = tweepy.Client(consumer_key='key',
                       consumer_secret='key',
                       access_token='key',
                       access_token_secret='key')


#Obsolete - this no longer works with v2
#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_token_secret)

#obsolete method to auth - works with v1
#api = tweepy.API(auth)

#Latest v2 method
#api = tweepy.Client(auth)


# Set up OpenAI API authentication
openai.api_key = os.getenv('OPENAI_API_KEY')
#openai.api_key='sk-key'


#sanity check for env variables
#print(os.getenv('consumer_key'))
#print(os.getenv('consumer_secret'))
#print(os.getenv('access_token'))
#print(os.getenv('access_token_secret'))



#Added prompts -kj
# Define a list of prompts
prompts = [
    "This is a test!"
]

# Updated Response to include desired values and prompt -kj
# Call the ChatGPT API using a random prompt from the list
prompt = prompts[random.randint(0, len(prompts)-1)]
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=20,
    n=1,
    stop=None,
    temperature=0.5,
)

# Extract the response from the API output
tweet_text = response.choices[0].text.strip()


# Added the user_approval var -kj
# Wait for user approval
user_approval = ""
while user_approval.upper() not in ["YES", "NO"]:
    user_approval = input("Did you approve the tweet and the image? (YES/NO): ")

# Post the tweet and image if approved
if user_approval.upper() == "YES":
    # Update the Twitter status with the image
    #api.update_status(status=tweet_text)
    client.create_tweet(text=tweet_text)
    print("Tweet posted successfully!")
else:
    print("Tweet not posted.")