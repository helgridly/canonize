# canonize
a tool for sifting through tweets

see the design doc: https://docs.google.com/document/d/1pE_3Kb1y5cpvGn1ZXR3OEhv9l9djObqSCIgCSTcDc34/edit?tab=t.0

## running locally

There's a decent chance that bundler or jekyll setup will stomp on existing files. If it does, revert their changes.

install:
```
sudo apt-get install ruby-full build-essential zlib1g-dev
gem install bundler
bundle init
bundle add jekyll
```

for local preview:
```
bundle exec jekyll serve
```

## now

- [x] clean up tweets.js into pile
- [x] synthesize tweets into conversations
- [x] TweetDetail graphql for finding missing parents
- [x] fetch tweet context from tweetpile.py
- [x] flatten conversations in depth-first tweet order
- [x] jekyll install + site setup
- [x] jekyll page template
- [x] twinder
- [ ] handle reviewed mark (incl. on convo update - see gdoc)

## next

- [ ] walk drafts and canon and extract jekyll front matter items (see codeium)
- [ ] explorer with filtering etc
- [ ] should tags link back to explorer?
- [ ] "random button" - how do we do "give me another", or do we not and just force user to browser back?
- [ ] domain
- [ ] write blurb text for home and about pages

# notes, design

- is only interested in YOUR tweets
- therefore if people respond to a thread after your last tweet, it might not show up in the conversation