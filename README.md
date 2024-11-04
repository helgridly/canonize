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
- [x] handle reviewed mark (incl. on convo update - see gdoc)
- [x] walk drafts and canon and extract jekyll front matter items (see codeium)
- [x] explorer with filtering etc
- [ ] add "show drafts" checkbox to explorer
- [ ] add "random button"

## next

- [ ] should tags link back to explorer?
- [ ] domain
- [ ] write blurb text for home and about pages
- [ ] make gen_contents.py a github action instead

# notes, design

- is only interested in YOUR tweets
- therefore if people respond to a thread after your last tweet, it might not show up in the conversation