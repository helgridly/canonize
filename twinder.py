import pdb
import textwrap
import html
import scratch
import tweetpile
import sortedcollections
import templates
import os
import slugify
import conf

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

def generate_draft(conv):
    user_tweets = [ t for t in conv if t['user_id'] == conf.USER_ID ]
    by_date = sorted(user_tweets, key=lambda t: t['date'])

    creation_date = by_date[0]['date']
    last_updated = by_date[-1]['date']
    mentions = list({ mention['username'] for tweet in conv for mention in tweet['mentions'] if mention['username'] != conf.USERNAME })
    sources = [by_date[0]['status_id']]

    # prompt for these
    title = input("enter a title for this post: ")
    tags = input("enter tags: ").split(", ")
    
    good_filename = False
    while(not good_filename):
        default_filename = slugify.slugify(title, stopwords=templates.stopwords)
        filename = input(f"enter filename, or hit Enter for {default_filename}: ") or default_filename
        if os.path.exists(f"drafts/{filename}.md"):
            overwrite = input("a draft file already exists with this name, overwrite it? (y/n): ")
            if overwrite != 'y':
                continue
        
        good_filename = True
    
    post = ""
    last_user = None
    for tweet in conv:
        if tweet['username'] != last_user:
            post += '`<' + tweet['username'] + ">` "
            post += html.unescape(tweet['text']).replace('\n', '  \n') + "  \n\n"
        else:
            post += html.unescape(tweet['text']).replace('\n', '  \n') + "  \n\n"
        last_user = tweet['username']

    file_contents = templates.canon.format(title=title,
                                           creation_date=creation_date,
                                           last_updated=last_updated,
                                           mentions=mentions,
                                           tags=tags,
                                           sources=sources,
                                           post=post)

    with open(f"drafts/{filename}.md", "w") as f:
        f.write(file_contents)
    print(f"wrote conversation to drafts/{filename}.md")

def review_conversations(conversations, reviewed):
    print(f"conversations to review: {len(conversations)}")
    for conv_id, conv in conversations.items():
        if conv_id not in reviewed or reviewed[conv_id] != { t['status_id'] for t in conv }:
            print_conversation(conv)
            keep = input("(k)eep or (s)kip? ") == 'k'
            if keep:
                generate_draft(conv)
            reviewed[conv_id] = reviewed.get(conv_id, set()) | { t['status_id'] for t in conv }
            scratch.save_reviewed(reviewed)

def excepthook(type, value, traceback):
    pdb.post_mortem(traceback)

def conv_is_reviewed(conv_id, conv, reviewed):
    """a conversation has been reviewed if we've already seen all the user's tweets"""
    if conv_id not in reviewed:
        return False
    
    conv_user_tweets = { t['status_id'] for t in conv if t['user_id'] == conf.USER_ID }
    return all( c in reviewed[conv_id] for c in conv_user_tweets )

if __name__ == "__main__":
    conversations = scratch.load_conversations()
    flat_convs = { k: tweetpile.conversation_to_flat_tree(v) for k, v in conversations.items() }

    # if you want to filter further (e.g. minimum 3 tweets from the user), do it here
    flat_convs = { k: v for k, v in flat_convs.items() if len([t for t in v if t['user_id'] == conf.USER_ID]) >= 3 }

    # filter out reviewed tweets
    reviewed = scratch.load_reviewed()
    unreviewed = { k: v for k, v in flat_convs.items() if not conv_is_reviewed(k, v, reviewed) }
    sorted_unreviewed = sortedcollections.ItemSortedDict(lambda k, v: tweetpile.find_earliest_user_tweet(v), unreviewed)

    review_conversations(sorted_unreviewed, reviewed)
