import tweepy
import openai
import random
import os
import requests
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

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

# Define a list of prompts
prompts = [
    "Write me a tweet about AI",
    "Write me a tweet about technology"
]

# Call the ChatGPT API using a random prompt from the list
prompt = prompts[random.randint(0, len(prompts)-1)]
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=280,
    n=1,
    stop=None,
    temperature=1,
)

# Extract the response from the API output
tweet_text = response.choices[0].text.strip()
print(tweet_text)
image_with_post = ""
while image_with_post.upper() not in ["YES", "NO"]:
    image_with_post = input("Do you want to generate an image with this post YES/NO: ")

# Post the tweet and image if approved
if image_with_post.upper() == "YES":
    # Prompt for a DALL-E image generation prompt
    image_prompt = f"generate me a twitter post that says a lot about the tech industry without saying anything at all"
    image_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=image_prompt,
        max_tokens=256,
        n=1,
        stop=None,
        temperature=1,
    )

    # Extract the response from the API output
    image_prompt = f"Geometric 3D rendering of, '{image_response.choices[0].text.strip()}'"
    print(image_prompt)

    # Generate the image from the DALL-E prompt
    url = 'https://api.openai.com/v1/images/generations'
    data = {
        'model': 'image-alpha-001',
        'prompt': image_prompt,
        'num_images': 1,
        'size': '512x512',
        'response_format': 'url'
    }

    headers = {'Authorization': f'Bearer {os.getenv("openai_api_key")}'}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    image_url = response.json()['data'][0]['url']

    # Download the image from the URL
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))

    # Preview the image and tweet
    image.show()

    # Wait for user approval
    user_approval = ""
    while user_approval.upper() not in ["YES", "NO"]:
        user_approval = input("Did you approve the tweet and the image? (YES/NO): ")

    # Post the tweet and image if approved
    if user_approval.upper() == "YES":
        # Save the image to a file
        image_path = 'image.png'
        image.save(image_path)

        # Update the Twitter status with the image
        media = api.media_upload(image_path)
        api.update_status(tweet_text, media_ids=[media.media_id])
        print("Tweet posted successfully!")
    else:
        print("Tweet not posted.")

else:
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