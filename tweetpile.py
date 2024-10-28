import json
import sortedcontainers
import conf
import datetime
import re

def parse_media(tweet):
    media = tweet.get('extended_entities', {}).get('media')
    if not media:
        return []
    else:
        return [m['media_url_https'] for m in media]

def get_qt_username(url):
    #import pdb; pdb.set_trace()
    match = re.search(r"https?://(twitter|x)\.com/([^/]+)/status/.*", url)
    if match:
        return match.group(2)
    else:
        return None

def parse_mentions(tweet):
    mentions = tweet.get('entities', {}).get('user_mentions')
    urls = tweet.get('entities', {}).get('urls')

    result = []
    if urls:
        for url in urls:            
            if (qt_user := get_qt_username(url['expanded_url'])):
                result.append({"username":qt_user}) # yikes, no id

    if mentions:
        result.extend([{"username": m['screen_name'], "user_id": m['id_str']} for m in mentions])

    return result

def parse_urls(tweet):
    urls = tweet.get('entities', {}).get('urls')
    if not urls:
        return []
    else:
        return [u['expanded_url'] for u in urls]


def parse_one_tweet(tweet):
    outweet = {
        "status_id" : tweet['id_str'],
        "username": conf.USERNAME,
        "user_id": conf.USER_ID,
        "media": parse_media(tweet),
        "parent_status_id": tweet.get('in_reply_to_status_id_str'),
        "parent_user_id": tweet.get('in_reply_to_user_id_str'),
        "parent_username": tweet.get('in_reply_to_screen_name'),
        "text" : tweet['full_text'],
        "mentions": parse_mentions(tweet),
        "urls": parse_urls(tweet),
        "date": datetime.datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S %z %Y")
    }
    return outweet

def create_sorted_tweetpile():
    """parse tweets.js into a list of tweets, sorted by date asc"""
    with open("tweets.js", "r") as f:
        contents = f.read()
        
        # they give us javascript with a variable assign at the beginning,
        # turn it into json
        javascript_prefix = "window.YTD.tweets.part0 = "
        if contents.startswith("window.YTD.tweets.part0 = "):
            contents = contents[len("window.YTD.tweets.part0 = "):]

        tweets = json.loads(contents)

    tweets_by_date = sortedcontainers.SortedList(key=lambda x: x['date'])
    for tweet in tweets:
        tweets_by_date.add(parse_one_tweet(tweet['tweet']))

    return tweets_by_date
