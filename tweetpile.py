import json
import sortedcollections
import conf
import datetime
import re
import itertools

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

def tweets_from_js(fname, js_prefix):
    """parse tweets.js into a list of tweets, sorted by status_id asc"""
    with open(fname, "r") as f:
        contents = f.read()
        
        # they give us javascript with a variable assign at the beginning,
        # turn it into json
        javascript_prefix = f"{js_prefix} = "
        if contents.startswith(javascript_prefix):
            contents = contents[len(javascript_prefix):]

        tweets = json.loads(contents)

    # ItemSortedDict is a dict whose keys can be ordered by their values
    # this means that when we iterate over the tweet ids, we get them back in status_id order,
    # which ascend over time
    tweets_by_status_id = sortedcollections.ItemSortedDict(lambda k, v: v['status_id'])
    for tweet in tweets:
        parsed = parse_one_tweet(tweet['tweet'])
        tweets_by_status_id.update({parsed['status_id'] : parsed})

    return tweets_by_status_id


def create_sorted_tweetpile():
    alive_tweets = tweets_from_js("tweets.js", "window.YTD.tweets.part0")
    deleted_tweets = tweets_from_js("deleted-tweets.js", "window.YTD.deleted_tweets.part0")

    alive_tweets.update(deleted_tweets)
    return alive_tweets

def pile_to_conversations(pile):
    """we have a pile of tweets that we want to turn into threads
    they come in status_id order, from oldest to newest. so we'll always see a parent tweet before its child
    
    - if a tweet has no parent, or its parent isn't from the user, make a new conversation for it
    - else label it with its parent's conversation_id and add it to that list
    """
    conversations = dict()

    for tweet_id in pile:
        tweet = pile[tweet_id]

        # if i'm a top level tweet, or my parent isn't the user, i'm the beginning of a new conversation
        if (not tweet['parent_status_id']) or (tweet['parent_user_id'] != conf.USER_ID):
            conversations[tweet_id] = [tweet]
            pile[tweet_id]['conversation_id'] = tweet_id

        # i'm a reply; add me to my parent's conversation
        else:
            parent = pile[tweet['parent_status_id']]
            tweet['conversation_id'] = parent['conversation_id']
            conversations[tweet['conversation_id']].append(tweet)

    # order conversations by the date of their first tweet
    sorted_convs = sortedcollections.ItemSortedDict(lambda k, v: v[0]['date'], conversations)
    return sorted_convs



if __name__ == "__main__":
    pile = create_sorted_tweetpile()
    conversations = pile_to_conversations(pile)
    import pdb; pdb.set_trace()
    pass
