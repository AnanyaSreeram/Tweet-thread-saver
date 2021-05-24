import tweepy
import time
import os
from dotenv import load_dotenv
load_dotenv()

def create_api():#authentication through tokens
    # CONSUMER_KEY = os.getenv('consumer_key')
    # CONSUMER_SECRET = os.getenv('consumer_secret')
    # AUTH_KEY = os.getenv('access_token')
    # AUTH_SECRET = os.getenv('access_token_secret')

    auth = tweepy.OAuthHandler(os.getenv("consumer_key"), os.getenv("consumer_secret"))
    auth.set_access_token(os.getenv("access_token"), os.getenv("access_token_secret"))

    global api
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    try:
        api.verify_credentials()
    except Exception as e:
        print("Error creating API")
        raise e

    return api


def client():
    mention = api.mentions_timeline(count=1)

    for tweet in mention:
        return tweet.user.id


def thread():
    x = open('mx.txt', 'r')
    m = x.readlines(1)
    for lines in m:
        return lines

def mention(api,since_id):
    new_since_id = since_id

    for tweet in tweepy.Cursor(api.mentions_timeline,since_id=since_id).items(50):


        new_since_id = max(tweet.id, new_since_id)

        if tweet.in_reply_to_status_id is not None:
            if not tweet.user.following:
                tweet.user.follow()

            status_id = tweet.in_reply_to_status_id
            tweet_u = api.get_status(status_id,tweet_mode='extended')

            print(tweet_u.full_text)
            f = open('mx.txt', 'w')
            f.write(tweet_u.full_text)
            f.close()

    return new_since_id



def main():
    api = create_api()
    since_id = 1
    print(since_id)
    print('the users info')
    a = mention(api,since_id)
    print(client())
    print(thread())
    api.send_direct_message(client(),thread())
    print('sent successfully')
    time.sleep(60)

if __name__ == "__main__":
    main()
