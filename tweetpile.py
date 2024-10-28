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
    """parse tweets.js into a list of tweets, sorted by date asc"""
    with open(fname, "r") as f:
        contents = f.read()
        
        # they give us javascript with a variable assign at the beginning,
        # turn it into json
        javascript_prefix = f"{js_prefix} = "
        if contents.startswith(javascript_prefix):
            contents = contents[len(javascript_prefix):]

        tweets = json.loads(contents)

    # ItemSortedDict is a dict whose keys can be ordered by their values
    # this means that when we iterate over the tweet ids, we get them back in date order
    # this doesn't guarantee that tweets are returned in the order they're written, because threads
    # written in the thread composer are published all at once and have identical dates :(
    tweets_by_date = sortedcollections.ItemSortedDict(lambda k, v: v['date'])
    for tweet in tweets:
        parsed = parse_one_tweet(tweet['tweet'])
        tweets_by_date.update({parsed['status_id'] : parsed})

    return tweets_by_date

def create_sorted_tweetpile():
    alive_tweets = tweets_from_js("tweets.js", "window.YTD.tweets.part0")
    deleted_tweets = tweets_from_js("deleted-tweets.js", "window.YTD.deleted_tweets.part0")

    alive_tweets.update(deleted_tweets)
    return alive_tweets

def pile_to_conversations(pile):
    """we have a pile of tweets that we want to turn into threads
    imagine a bunch of empty hangers.
    every time we see a tweet, we:
        - see if there's a hanger labelled with its id. if so, mark its conv_id as itself
        then:
        - if the tweet has no parent, set its conv_id as itself
        - if the tweet has a parent:
            - if the parent is from me, and the parent already has a conv_id, inherit the parent's conv_id
                - if we already had a conv_id, find all other tweets on that hanger and move them; delete the old conv_id
            - if the parent is from me, and doesn't have a conv_id yet, 
            - if the parent isn't from me, set its conv_id as itself [we'll fix this with the lookup]
    """
    
    conversations = dict()

    for tweet_id in pile:
        tweet = pile[tweet_id]

        # if another tweet marked me as the head of a conversation, become the head of that conversation
        if tweet_id in conversations:
            tweet['conversation_id'] = tweet_id
            conversations[tweet_id] = [tweet] + conversations[tweet_id]

        # if nobody marked me as the head of a conversation, but i'm a top level tweet, i'm the beginning of a new conversation
        elif not tweet['parent_status_id']:
            conversations[tweet_id] = [tweet]
            pile[tweet_id]['conversation_id'] = tweet_id

        # i'm a reply; walk up the chain
        if tweet['parent_status_id']:
            old_conv_id = tweet.get('conversation_id')

            # if the parent is from our user, we've either seen it already, or will eventually
            if tweet['parent_user_id'] == conf.USER_ID:
                parent = pile[tweet['parent_status_id']]

                # we've seen the parent already, join its conversation
                if 'conversation_id' in parent:
                    tweet['conversation_id'] = parent['conversation_id']

                # we haven't seen the parent yet. make a conversation for it
                else:
                    tweet['conversation_id'] = tweet['parent_status_id']
                    conversations[tweet['parent_status_id']] = [] # we'll move everything in a sec
                
            # the parent is not from our user. this is the horrible lookup case
            else:
                # for now, we'll treat it as a top level tweet
                tweet['conversation_id'] = tweet_id
                conversations[tweet_id] = [] # we'll move everything in a sec

            if old_conv_id is not tweet['conversation_id']:
                if not old_conv_id:
                    # no old conversation, just add us to the new conversation 
                    #if tweet_id == '1850299977123197017':
                    #    import pdb; pdb.set_trace()
                    #    pass
                    conversations[tweet['conversation_id']].append(tweet)
                else:
                    # move us and all our children to the new conversation id
                    try:
                        assert tweet in conversations[old_conv_id]
                    except AssertionError as e:
                        import pdb; pdb.set_trace()
                        pass
                    conversations[tweet['conversation_id']].extend( conversations[old_conv_id] )
                    del conversations[old_conv_id]
                    

                for t in conversations[tweet['conversation_id']]:
                    t['conversation_id'] = tweet['conversation_id']

    # order posts in conversations by status id (which ascend over time, good enough)
    for c in conversations:
        conversations[c] = sorted(conversations[c], key=lambda t: t['status_id'])

    # at the end: order conversations by the date of their first tweet
    #conversations = {sortedcollections.ItemSortedDict(lambda k, v: v[0]['date'])}

    return conversations



if __name__ == "__main__":
    pile = create_sorted_tweetpile()
    conversations = pile_to_conversations(pile)
    import pdb; pdb.set_trace()
    pass
