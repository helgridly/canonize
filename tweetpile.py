import json
import sortedcollections
import conf
import scratch
import tweetparse
import graphql
import sys
import pdb
import copy

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
        parsed = tweetparse.parse_one_tweet(tweet['tweet'])
        tweets_by_status_id.update({parsed['status_id'] : parsed})

    return tweets_by_status_id


def create_sorted_tweetpile():
    # TODO: there's also note-tweet.js, for long tweets, and community-tweet.js, for communities
    # i don't have either of these so i don't care. but could merge them with alive_tweets
    alive_tweets = tweets_from_js("input/tweets.js", "window.YTD.tweets.part0")
    deleted_tweets = tweets_from_js("input/deleted-tweets.js", "window.YTD.deleted_tweets.part0")

    alive_tweets.update(deleted_tweets)
    return alive_tweets

def conversation_to_flat_tree(conv_tweets):
    def recursive_flatten(tweet):
        result = [tweet]
        for child in conv_tweets:
            if child['parent_status_id'] == tweet['status_id']:
                result.extend(recursive_flatten(child))
        return result

    # remove dupes
    status_ids = set()
    deduped_conv = []
    for tweet in conv_tweets:
        if tweet["status_id"] not in status_ids:
            status_ids.add(tweet["status_id"])
            deduped_conv.append(tweet)

    root_tweets = [tweet for tweet in deduped_conv if tweet['parent_status_id'] is None]
    return [tweet for root in root_tweets for tweet in recursive_flatten(root)]

def find_earliest_user_tweet(conv):
    for tweet in conv:
        if tweet['user_id'] == conf.USER_ID and tweet['date']:
            return tweet['date']
    return None

def pile_to_conversations(pile):
    """we have a pile of tweets that we want to turn into threads
    they come in status_id order, from oldest to newest. so we'll always see a parent tweet before its child
    
    - if a tweet has no parent, or its parent isn't from the user, make a new conversation for it
    - else label it with its parent's conversation_id and add it to that list
    """

    # resume
    conversations = scratch.load_conversations()
    old_conversations = copy.deepcopy(conversations)

    context_pile = scratch.load_context_pile()
    last_tweet_id = scratch.load_tweetpile_resume()
    pile_index = pile.keys().index(last_tweet_id) if last_tweet_id else 0

    # if resuming, populate the tweet pile with conversation_ids
    for conv_id in conversations:
        for tweet in conversations[conv_id]:
            if tweet['user_id'] == conf.USER_ID:
                pile[tweet['status_id']]['conversation_id'] = conv_id

    for tweet_id in pile.keys()[pile_index:]:
        tweet = pile[tweet_id]

        # if i'm a top level tweet, i'm the beginning of a new conversation
        if not tweet['parent_status_id']:
            conversations[tweet_id] = [tweet]
            pile[tweet_id]['conversation_id'] = tweet_id
            continue

        # if i have a parent, but it's not the user, it won't be in the twitter export
        elif tweet['parent_user_id'] != conf.USER_ID:
            if tweet['parent_status_id'] not in context_pile:
                # we don't know of this tweet and will have to fetch it
                # fetch_tweet_context updates the context_pile with the parent tweet and all the ones above it
                # returns a conversation id and a list of tweets to add to the conversation
                print("looking for parent tweet", tweet['parent_status_id'], "for tweet", tweet['status_id'])
                conv_id, conv_tweet_ids = graphql.fetch_tweet_context(tweet['parent_status_id'], context_pile, pile)
                
                # found a new conversation
                if conv_id not in conversations:
                    conversations[conv_id] = []

                # add the parent and everything above it to the conversation
                for t_id in conv_tweet_ids:
                    context_pile[t_id]['conversation_id'] = conv_id
                    conversations[conv_id].append(context_pile[t_id])
            
            # now the parent is definitely in the context pile
            parent = context_pile[tweet['parent_status_id']]

        # i'm a reply to a user's tweet
        else:
            parent = pile[tweet['parent_status_id']]

        tweet['conversation_id'] = parent['conversation_id']
        conversations[tweet['conversation_id']].append(tweet)

        scratch.save_conversations(conversations)
        scratch.save_context_pile(context_pile)
        scratch.save_tweetpile_resume(tweet['status_id'])

    # flatten each conversation
    # order conversations by the date of their first tweet
    flat_convs = { k: conversation_to_flat_tree(v) for k, v in conversations.items() }
    sorted_convs = sortedcollections.ItemSortedDict(lambda k, v: find_earliest_user_tweet(v), flat_convs)
    return sorted_convs


def excepthook(type, value, traceback):
    pdb.post_mortem(traceback)

if __name__ == "__main__":
    sys.excepthook = excepthook
    pile = create_sorted_tweetpile()
    conversations = pile_to_conversations(pile)
    print("done!")

