import scratch

# i wrote this script because i spelled my own username wrong in the conf
# you should not need it

def fix_one_tweet(tweet):
    if tweet['username'] == "seflathing":
        tweet['username'] = "selflathing"
    
    if tweet['parent_username'] == "seflathing":
        tweet['parent_username'] = "selflathing"
    
    for mention in tweet['mentions']:
        if mention['username'] == "seflathing":
            mention['username'] = "selflathing"
    
    return tweet

if __name__ == "__main__":
    # fix context pile
    context_pile = scratch.load_context_pile()

    for tweet_id, tweet in context_pile.items():
        fix_one_tweet(tweet)

    scratch.save_context_pile(context_pile)

    # fix conversations
    conversations = scratch.load_conversations()

    for conv_id, conv in conversations.items():
        for tweet in conv:
            fix_one_tweet(tweet)

    scratch.save_conversations(conversations)
