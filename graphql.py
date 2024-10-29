import secrets
import requests
import json
import urllib.parse
import tweetparse

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

def fetch_tweet_detail(focalTweetId, cursor=None):
    resp = requests.get("https://x.com/i/api/graphql/nBS-WpgA6ZG0CyNHD517JQ/TweetDetail", params=get_params(focalTweetId, cursor), headers=get_headers()).json()

    tweets = [] # tuples of tweet, user data
    cursors = {} # tuples of cursor type, value

    for instr in resp['data']['threaded_conversation_with_injections_v2']['instructions']:
        if instr['type'] == "TimelineAddEntries":
            for entry in instr['entries']:
                if entry['content']['entryType'] == "TimelineTimelineItem":
                    itemContent = entry['content']['itemContent']
                
                    if itemContent['itemType'] == "TimelineTimelineCursor":
                        cursors[itemContent['cursorType']] = itemContent['value']
                        # print("TC", itemContent['cursorType'], itemContent['value'] )

                    elif itemContent['itemType'] == "TimelineTweet":
                        tweets.append(raw_tweet_to_parsed(itemContent['tweet_results']['result']))
                        #print("TI", itemContent['tweet_results']['result']['legacy']['full_text'] )
                    
                # timeline modules are boxes with more tweets in them, sometimes called "profile conversations"
                elif entry['content']['entryType'] == "TimelineTimelineModule":
                    for item in entry['content']['items']:
                        itemContent = item['item']['itemContent']

                        if itemContent['itemType'] == "TimelineTimelineCursor":
                            cursors[itemContent['cursorType']] = itemContent['value']
                            # print("TM-cursor", itemContent['cursorType'], itemContent['value'])
                        
                        elif itemContent['itemType'] == "TimelineTweet":
                            tweets.append(raw_tweet_to_parsed(itemContent['tweet_results']['result']))
                            #print("TM", itemContent['tweet_results']['result']['legacy']['full_text'] )

    return (tweets, cursors)

if __name__ == "__main__":
    # TODO: receive a context pile and the tweet pile
    # fetch tweet details
    # work bottom to top, putting it all in the context pile and stopping when we hit something by the user that's NOT the focused tweet
    # paginate upwards using cursorTop if we hit the top before finding anything
    #   ==> remember to ratelimit pagination
    # return the expanded context pile and tweetpile.py will take it from there
    
    tweets, cursors = fetch_tweet_detail("1850670820894421069", "DwAAAPAAHCaEgLn98s7crjM1AgAA")

    import pdb; pdb.set_trace()
    pass


