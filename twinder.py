import itertools
import pdb
import textwrap
import html
import tweetpile
import sortedcollections

def print_tweet(tweet, last_user):
    max_username_length = 15
    max_username_space = max_username_length + 2 # 15 max length, plus "> "
    max_line_length = 100

    if tweet['username'] == last_user:
        prompt = " "*(max_username_space)
    else:
        # redraw the prompt
        prompt = tweet['username'] + "> " + " "*(max_username_length - len(tweet['username']))

    # textwrap does funny things to newlines, and recommends calling splitlines first, then wrapping each line
    tweet_lines = html.unescape(tweet['text']).splitlines()

    # prompt + first line
    lines = textwrap.wrap(prompt + tweet_lines[0], width = max_line_length)
    print(lines[0])
    if len(lines) > 1:
        rest = " ".join(lines[1:])
        print(textwrap.indent(textwrap.fill(rest, width = max_line_length - max_username_space), " "*(max_username_space)))

    # everything else
    if len(tweet_lines) > 1:
        for line in tweet_lines[1:]:
            print(textwrap.indent(textwrap.fill(line, width = max_line_length - max_username_space), " "*(max_username_space)))

    # tweet id + reply details
    if tweet.get('parent_status_id') and tweet['parent_user_id'] != tweet['user_id']:
        reply_suffix = " @" + tweet['parent_username'] + " " + tweet['parent_status_id']
    else:
        reply_suffix = ''
    
    print(textwrap.indent(str(tweet['status_id']) + reply_suffix, " "*(max_username_space)))
    print('')

def print_conversation(conv):
    print(tweetpile.find_earliest_user_tweet(conv))
    last_user = None
    for tweet in conv:
        print_tweet(tweet, last_user)
        last_user = tweet['username']
    print('')

def excepthook(type, value, traceback):
    pdb.post_mortem(traceback)

if __name__ == "__main__":
    conversations = tweetpile.load_conversations()

    flat_convs = { k: tweetpile.conversation_to_flat_tree(v) for k, v in conversations.items() }
    sorted_convs = sortedcollections.ItemSortedDict(lambda k, v: tweetpile.find_earliest_user_tweet(v), flat_convs)

    # TODO: given a conversation, generate a markdown page that looks like qualified-immunity.md
    # ask for filename, tags, title
    # generate creation + last updated date (user tweets, not everyone), mentions, source ID (earliest user tweet), conversation id
    # check to see if you're about to stomp on filename and ask are you sure
    # render, and write to drafts/
    # mark convo id as reviewed in scratch/

    for conv_id, conv in conversations.items():
        print_conversation(conv)
        pdb.set_trace()
    pass
