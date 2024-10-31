import json
import sortedcollections
import conf
import datetime
import re
import itertools
import tweetparse
import graphql
import sys
import pdb
import pickle

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
    alive_tweets = tweets_from_js("tweets.js", "window.YTD.tweets.part0")
    deleted_tweets = tweets_from_js("deleted-tweets.js", "window.YTD.deleted_tweets.part0")

    alive_tweets.update(deleted_tweets)
    return alive_tweets

def save_conversations(conversations):
    with open("conversations.pkl", "wb") as f:
        pickle.dump(conversations, f)

def load_conversations():
    # if we have a conversations.pkl file, load it
    try:
        with open("conversations.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}

def save_context_pile(context_pile):
    with open("context_pile.pkl", "wb") as f:
        pickle.dump(context_pile, f)

def load_context_pile():
    # if we have a context_pile.pkl file, load it
    try:
        with open("context_pile.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}

def save_tweetpile_resume(status_id):
    with open("tweetpile_resume", "w") as f:
        f.write(status_id)

def load_tweetpile_resume():
    try:
        with open("tweetpile_resume", "r") as f:
            return f.read()
    except FileNotFoundError:
        return 0

def pile_to_conversations(pile):
    """we have a pile of tweets that we want to turn into threads
    they come in status_id order, from oldest to newest. so we'll always see a parent tweet before its child
    
    - if a tweet has no parent, or its parent isn't from the user, make a new conversation for it
    - else label it with its parent's conversation_id and add it to that list
    """

    # resume
    conversations = load_conversations()
    context_pile = load_context_pile()
    last_tweet_id = load_tweetpile_resume()
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

        save_conversations(conversations)
        save_context_pile(context_pile)
        save_tweetpile_resume(tweet['status_id'])

    # TODO: instead flatten the tree depth-first to maintain thread ordering better, see codeium
    # order conversations by the date of their first tweet
    sorted_convs = sortedcollections.ItemSortedDict(lambda k, v: v[0]['date'], conversations)
    return sorted_convs


def excepthook(type, value, traceback):
    pdb.post_mortem(traceback)


if __name__ == "__main__":
    sys.excepthook = excepthook
    pile = create_sorted_tweetpile()
    conversations = pile_to_conversations(pile)

    # OK whatever - we have to debug something that's going screwy here, but i'm tired and outta time for the day
    # https://x.com/polyascension/status/1770698268562858297

    # some ideas that'll help The Big Debug:
    # - truncate or subset the tweet pile
    # - save off the context pile as you go
    
    pdb.set_trace()
    pass
