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

- [ ] do some reviewing and create some articles!
- [ ] document the process in this readme

## later

- [ ] domain
- [ ] add "random button"
- [ ] make gen_contents.py a github action instead


## done

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
- [x] add "show drafts" checkbox to explorer
- [x] write blurb text for home and about pages
- [x] fix date sorting
- [x] GitHub codespaces; install python + ruby devcontainer features


# notes, design

- is only interested in YOUR tweets
- therefore if people respond to a thread after your last tweet, it might not show up in the conversation
