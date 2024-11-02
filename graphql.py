import secrets
import requests
import json
import urllib.parse
import tweetparse
import time
import conf

# trash we have to pass to twitter otherwise it gets mad
default_features = {
    'c9s_tweet_anatomy_moderator_badge_enabled': True,
    'responsive_web_home_pinned_timelines_enabled': True,
    'blue_business_profile_image_shape_enabled': True,
    'creator_subscriptions_tweet_preview_api_enabled': True,
    'freedom_of_speech_not_reach_fetch_enabled': True,
    'graphql_is_translatable_rweb_tweet_is_translatable_enabled': True,
    'graphql_timeline_v2_bookmark_timeline': True,
    'hidden_profile_likes_enabled': True,
    'highlights_tweets_tab_ui_enabled': True,
    'interactive_text_enabled': True,
    'longform_notetweets_consumption_enabled': True,
    'longform_notetweets_inline_media_enabled': True,
    'longform_notetweets_rich_text_read_enabled': True,
    'longform_notetweets_richtext_consumption_enabled': True,
    'profile_foundations_tweet_stats_enabled': True,
    'profile_foundations_tweet_stats_tweet_frequency': True,
    'responsive_web_birdwatch_note_limit_enabled': True,
    'responsive_web_edit_tweet_api_enabled': True,
    'responsive_web_enhance_cards_enabled': False,
    'responsive_web_graphql_exclude_directive_enabled': True,
    'responsive_web_graphql_skip_user_profile_image_extensions_enabled': False,
    'responsive_web_graphql_timeline_navigation_enabled': True,
    'responsive_web_media_download_video_enabled': False,
    'responsive_web_text_conversations_enabled': False,
    'responsive_web_twitter_article_data_v2_enabled': True,
    'responsive_web_twitter_article_tweet_consumption_enabled': False,
    'responsive_web_twitter_blue_verified_badge_is_enabled': True,
    'rweb_lists_timeline_redesign_enabled': True,
    'rweb_video_timestamps_enabled': True,
    'rweb_tipjar_consumption_enabled': False,
    'communities_web_enable_tweet_community_results_fetch': True,
    'creator_subscriptions_quote_tweet_preview_enabled': True,
    'articles_preview_enabled': True,
    'spaces_2022_h2_clipping': True,
    'spaces_2022_h2_spaces_communities': True,
    'standardized_nudges_misinfo': True,
    'subscriptions_verification_info_verified_since_enabled': True,
    'tweet_awards_web_tipping_enabled': False,
    'tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled': True,
    'tweetypie_unmention_optimization_enabled': True,
    'verified_phone_label_enabled': False,
    'vibe_api_enabled': True,
    'view_counts_everywhere_api_enabled': True
}
default_variables = {
    'count': 1000,
    'withSafetyModeUserFields': True,
    'includePromotedContent': False,
    'withQuickPromoteEligibilityTweetFields': True,
    'withVoice': True,
    'withV2Timeline': True,
    'withDownvotePerspective': False,
    'withBirdwatchNotes': True,
    'withCommunity': True,
    'withSuperFollowsUserFields': True,
    'withReactionsMetadata': False,
    'withReactionsPerspective': False,
    'withSuperFollowsTweetFields': True,
    'isMetatagsQuery': False,
    'withReplays': True,
    'withClientEventToken': False,
    'withAttachments': True,
    'withConversationQueryHighlights': True,
    'withMessageQueryHighlights': True,
    'withMessages': True,
}

def get_headers():
    return {
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs=1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        'cookie': '; '.join(f'{k}={v}' for k, v in secrets.cookies.items()),
        'referer': 'https://twitter.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'x-csrf-token': secrets.cookies.get('ct0', ''),
        'x-twitter-auth-type': 'OAuth2Session',
        'x-twitter-active-user': 'yes',
        'x-twitter-client-language': 'en',
        'Accept-Encoding': 'gzip, deflate'
    }

def get_params(focalTweetId, cursor=None):
    gql_vars = {
        "focalTweetId":focalTweetId,
        "referrer":"tweet"
        }
    if cursor:
        gql_vars['cursor'] = cursor

    vars_str = json.dumps(gql_vars | default_variables, separators=(',', ':')) 
    feats_str = json.dumps(default_features, separators=(',', ':'))

    return {"variables": vars_str, "features": feats_str} #urllib.parse.quote(vars_str)}


#variables=%7B%22focalTweetId%22%3A%221850670820894421069%22%2C%22cursor%22%3A%22DwAAAPAAHCaEgLn98s7crjM1AgAA%22%2C%22referrer%22%3A%22tweet%22%2C%22with_rux_injections%22%3Afalse%2C%22rankingMode%22%3A%22Relevance%22%2C%22includePromotedContent%22%3Atrue%2C%22withCommunity%22%3Atrue%2C%22withQuickPromoteEligibilityTweetFields%22%3Atrue%2C%22withBirdwatchNotes%22%3Atrue%2C%22withVoice%22%3Atrue%7D
#https://x.com/i/api/graphql/nBS-WpgA6ZG0CyNHD517JQ/TweetDetail?variables=%7B%22focalTweetId%22%3A%221850670820894421069%22%2C%22with_rux_injections%22%3Afalse%2C%22rankingMode%22%3A%22Relevance%22%2C%22includePromotedContent%22%3Atrue%2C%22withCommunity%22%3Atrue%2C%22withQuickPromoteEligibilityTweetFields%22%3Atrue%2C%22withBirdwatchNotes%22%3Atrue%2C%22withVoice%22%3Atrue%7D&features=%7B%22rweb_tipjar_consumption_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22communities_web_enable_tweet_community_results_fetch%22%3Atrue%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22articles_preview_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Atrue%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22creator_subscriptions_quote_tweet_preview_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22rweb_video_timestamps_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D&fieldToggles=%7B%22withArticleRichContentState%22%3Atrue%2C%22withArticlePlainText%22%3Afalse%2C%22withGrokAnalyze%22%3Afalse%2C%22withDisallowedReplyControls%22%3Afalse%7D


def raw_tweet_to_parsed(tweet_result):
    return tweetparse.parse_one_tweet(tweet_result['legacy'], tweet_result['core']['user_results']['result'])

def deleted_tweet_to_parsed(str_id):
    return dead_tweet_to_parsed(str_id, True, None)

def tombstone_tweet_to_parsed(tweet_result, entry, parent_tweet):
    is_deleted = "deleted" in tweet_result['tombstone']['text']['text']
    return dead_tweet_to_parsed(entry['entryId'].split('-')[-1], is_deleted, parent_tweet)

DELETED_REST_ID = -1
LOCKED_REST_ID = 0
def dead_tweet_to_parsed(id_str, is_deleted, parent_tweet):
    dummy_user_data = {
        "rest_id": DELETED_REST_ID if is_deleted else LOCKED_REST_ID,
        "legacy": {
            "screen_name": "[deleted]" if is_deleted else "[locked]",
        }
    }
    dummy_tweet = {
        "id_str": id_str,
        "in_reply_to_status_id_str": parent_tweet and parent_tweet['status_id'],
        "in_reply_to_user_id_str": parent_tweet and parent_tweet['user_id'],
        "in_reply_to_screen_name": parent_tweet and parent_tweet['username'],
        "full_text": "[deleted]" if is_deleted else "[locked]",
        "created_at": None
    }
    return tweetparse.parse_one_tweet(dummy_tweet, dummy_user_data)

rate_limit_remaining = 150
rate_limit_reset = 0
def ratelimit_wait():
    print("Rate limit remaining", rate_limit_remaining, "reset in", rate_limit_reset - time.time(), "seconds")
    now = time.time()
    if rate_limit_remaining < 10 and now < rate_limit_reset:
        print("Rate limit, sleeping", (rate_limit_reset - now) + 5, "seconds")
        time.sleep((rate_limit_reset - now) + 5)

def update_ratelimit(headers):
    global rate_limit_remaining
    global rate_limit_reset
    rate_limit_remaining = int(headers['x-rate-limit-remaining'])
    rate_limit_reset = int(headers['x-rate-limit-reset'])

def parse_one_tweet(tweets, entry, is_module=False):
    item = entry['item' if is_module else 'content']
    itemContent = item['itemContent']
    new_cursors = {}
    new_tweets = []

    if itemContent['itemType'] == "TimelineTimelineCursor":
        new_cursors[itemContent['cursorType']] = itemContent['value']
        # print("TM-cursor" if is_module else "TI-cursor", itemContent['cursorType'], itemContent['value'] )
    
    elif item.get('clientEventInfo', {}).get('component', '') == "related_tweet":
        # no! bad twitter! don't inject things not in the conversation into the conversation!!!!!
        pass
    
    elif itemContent['itemType'] == "TimelineTweet" and itemContent['tweet_results']: # sometimes tweet_results is empty(!!!)

        # deleted tweet or locked account
        if itemContent['tweet_results']['result']['__typename'] == "TweetTombstone":
            new_tweets.append(tombstone_tweet_to_parsed(itemContent['tweet_results']['result'],
                                                        entry,
                                                        tweets[-1] if tweets else None))
            #print("TM" if is_module else "TI", [tombstone] )
        elif itemContent['tweet_results']['result']['__typename'] == "TweetWithVisibilityResults":
            # for "people the author mentioned can reply" type tweets
            new_tweets.append(raw_tweet_to_parsed(itemContent['tweet_results']['result']['tweet']))
            #print("TM" if is_module else "TI", itemContent['tweet_results']['result']['tweet']['legacy']['full_text'] )
        else:
            new_tweets.append(raw_tweet_to_parsed(itemContent['tweet_results']['result']))
            #print("TM" if is_module else "TI", itemContent['tweet_results']['result']['legacy']['full_text'] )
    
    return new_cursors, new_tweets

def fetch_tweet_detail(focalTweetId, cursor=None):
    ratelimit_wait()
    print("fetching", focalTweetId, "at cursor", cursor if cursor else "<none>")
    resp = requests.get("https://x.com/i/api/graphql/nBS-WpgA6ZG0CyNHD517JQ/TweetDetail", params=get_params(focalTweetId, cursor), headers=get_headers())
    update_ratelimit(resp.headers)
    result = resp.json()

    tweets = [] # tuples of tweet, user data
    cursors = {} # tuples of cursor type, value

    # handle missing top-level tweets, which when you look them up give you a big ole nope instead of a tombstone
    if any( ["No status found" in error.get('message', "") for error in result.get('errors', [])] ):
        tweets.append(deleted_tweet_to_parsed(focalTweetId))
        return (tweets, cursors)

    for instr in result['data']['threaded_conversation_with_injections_v2']['instructions']:
        if instr['type'] == "TimelineAddEntries":
            for idx, entry in enumerate(instr['entries']):
                if entry['content']['entryType'] == "TimelineTimelineItem":
                    new_cursors, new_tweets = parse_one_tweet(tweets, entry)
                    cursors.update(new_cursors)
                    tweets.extend(new_tweets)
                    
                # timeline modules are boxes with more tweets in them, sometimes called "profile conversations"
                elif entry['content']['entryType'] == "TimelineTimelineModule":
                    for item in entry['content']['items']:
                        new_cursors, new_tweets = parse_one_tweet(tweets, item, is_module=True)
                        cursors.update(new_cursors)
                        tweets.extend(new_tweets)

    return (tweets, cursors)

def fetch_tweet_context(tweet_id, context_pile, tweet_pile):
    """
    calls TweetDetails, paginating upwards, until we find a tweet we already know about
    adds all tweets it encounters to the context_pile
    returns a conversation id, and a list of tweets to add to the conversation
    """
    # list of tweets we've added to the context pile from this conversation
    conversation_tweets_ids = []
    cursor = None
    known_parent_tweet = None

    while True:
        tweets, cursors = fetch_tweet_detail(tweet_id, cursor)

        # go in reverse order
        for tweet in tweets[::-1]:
            print(tweet['status_id'], tweet['text'][:50])

            if tweet['status_id'] in context_pile or tweet['status_id'] in tweet_pile:

                # note that tweet detail sometimes returns tweets AFTER the focused tweet id,
                # including potentially tweets from the user which REALLY messes things up
                # hence the check for status_id < tweet_id - we only care if it's an earlier tweet
                # we do still add it to the context pile and conversation though
                if tweet['status_id'] < tweet_id:

                    # it's either someone else's tweet that we've seen before, or
                    # it's one of our tweets (which we have also seen before)
                    known_parent_tweet = tweet_pile.get(tweet['status_id']) or context_pile.get(tweet['status_id'])

                    # it should have a conversation id, in which case we're done                    
                    try:
                        assert known_parent_tweet and known_parent_tweet.get('conversation_id')
                    except AssertionError as e:
                        import pdb; pdb.set_trace()
                        pass

                    break
            
            if tweet['status_id'] == "1761502917972938761":
                #import pdb; pdb.set_trace()
                pass

            if tweet['user_id'] != conf.USER_ID:
                # if we've scanned ahead of focusedTweetId then we might find one of our own tweets,
                # which we don't want to add to the context pile
                conversation_tweets_ids.append(tweet['status_id'])
                context_pile[tweet['status_id']] = tweet

        if not known_parent_tweet:
            # we got to the first tweet in the thread
            if 'Top' in cursors:
                # keep paginating upwards
                cursor = cursors['Top']
                continue
            else:
                # if we hit the top and don't have a cursor, then the first tweet is the new conversation id
                known_parent_tweet = tweets[0]
                known_parent_tweet['conversation_id'] = known_parent_tweet['status_id']

        return known_parent_tweet['conversation_id'], conversation_tweets_ids
    
    assert False, "shouldn't get here"
    return (conversation_id, conversation_tweets_ids)



if __name__ == "__main__":
    # testing
    import pdb; pdb.set_trace()    
    tweets, cursors = fetch_tweet_detail("1850260126638489707")
    context_pile = {}
    tweet_pile = {}
    conv_id, conv_tweet_ids = fetch_tweet_context("1850670820894421069", context_pile, tweet_pile)

    import pdb; pdb.set_trace()
    pass
