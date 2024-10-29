import conf
import re
import datetime

def parse_media(tweet):
    media = tweet.get('extended_entities', {}).get('media')
    if not media:
        return []
    else:
        return [m['media_url_https'] for m in media]

def get_qt_username(url):
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

def parse_one_tweet(tweet, user_data = None):
    if user_data:
        user_id = user_data['rest_id']
        username = user_data['legacy']['screen_name']
    else:
        user_id = conf.USER_ID
        username = conf.USERNAME

    outweet = {
        "status_id" : tweet['id_str'],
        "username": username,
        "user_id": user_id,
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
