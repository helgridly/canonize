

def graphql_get_thread(status_id):
    """use TweetDetail to get the full list of tweets in the thread, including by other poster
    pull the tweets, make 'em look like my data structure, dump 'em in the pile

    get what you get, and paginate up - that's the direction of the parent tweet you care about
    stop paginating when you either see a tweet by the user or one that's already in the context pile    

    try https://github.com/trevorhobenshield/twitter-api-client

    i am not sure if this client uses the top cursor - test it
    here's one with lots of up, the browser makes 3 TweetDetail calls as you scroll
    https://x.com/swampentity/status/1850670820894421069

    i bet this won't work; eventually there is no cursor-top in the response, you get
    TimelineTerminateTimeline instead

    USE AN ALT ACCOUNT
    """
    pass
