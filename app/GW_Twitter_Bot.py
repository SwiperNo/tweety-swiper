import tweepy
import openai
import random
import os
from dotenv import load_dotenv

load_dotenv("C:\\Users\\kjon5\\repos\\tweety-swiper\\.env")

# Set up Twitter API authentication
consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Set up OpenAI API authentication
openai.api_key = os.getenv('openai_api_key')

#Added prompts -kj
# Define a list of prompts
prompts = [
    "This is a test!",
    "Hello, World!",
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
    api.update_status(tweet_text)
    print("Tweet posted successfully!")
else:
    print("Tweet not posted.")