# canonize
a tool for sifting through tweets

see the design doc: https://docs.google.com/document/d/1pE_3Kb1y5cpvGn1ZXR3OEhv9l9djObqSCIgCSTcDc34/edit?tab=t.0

## now

- [x] clean up tweets.js into pile
- [x] synthesize tweets into conversations
- [x] TweetDetail graphql for finding missing parents
- [ ] fetch tweet context from tweetpile.py
- [ ] flatten conversations in depth-first tweet order

## next

- [ ] jekyll page template
- [ ] twinder
- [ ] remove reviewed mark
- [ ] stand up jekyll site
- [ ] explorer with filtering etc

# notes, design

- is only interested in YOUR tweets
- therefore if people respond to a thread after your last tweet, it might not show up in the conversation