# canonize

canonize is a tool to help review your tweets, turn them into Writing, and host them on a Jekyll site.

## installation

You need Python 3.something and Ruby of some kind.

### locally

install:
```
sudo apt-get install ruby-full build-essential zlib1g-dev
gem install bundler
bundle init
bundle install
pip install -r requirements.txt
```

There's a decent chance that bundler or jekyll setup will stomp on existing files. If it does, revert their changes.

for local preview:
```
bundle exec jekyll serve
```

### devcontainer

If you prefer a devcontainer or GitHub codespaces, that works too. For some reason the `pip install -r requirements.txt` command doesn't work but you can just run it yourself.

## running canonize

### first time setup

- Delete everything in the `drafts/` and `canon/` folders 
- Request and download your Twitter archive
- Unzip `tweets.js` and `deleted-tweets.js`into a subdirectory of this repo called `input/`
- Make an empty directory called `scratch/`
- Open Twitter in your browser, open Dev Tools, and find the `auth_token` and `ct0` values from a `Cookie:` header
- Create a file in the root of this repository called `secrets.py` with the following contents, and fill them in:

```
cookies = {
    "auth_token": "XXXX",
    "ct0": "XXXX"
}
```

These seem to last a long time (weeks?).

### parse your tweets and fetch context

- Run `python tweetpile.py`.

This will walk all your tweets and query Twitter for other people's tweets in the conversation.

This takes a while (hours) because Twitter has a ratelimit of 150 requests every 15 minutes.

You can safely Ctrl+C out of the process and it'll pick up where it left off next time you run.

### decide which tweets you like

- Run `python twinder.py`.

twinder is "tinder for your tweets". Each Twitter thread you've contributed to will be shown to you, and you'll be prompted to keep it or skip it. If you keep it, it'll ask you for an article name and some tags, and will output a markdown file with the thread and some metadata into the `drafts/` directory.

canonize is only interested in _your_ tweets, so if other people have posted in the thread after your last tweet, they might not show up in the reviewer. However, twinder prints each tweet's status ID, which you can copy to your browser and stick at the end of `twitter.com/any_username/status/<the_id>` to look it up.

You can safely Ctrl+C out of the process and it'll pick up where it left off next time you run.

### it's up to you from here on out

You now have a `drafts/` folder full of Twitter threads. What you want to do with them is up to you!

My process is something like:
- I mark a thread as "keep" and edit its draft markdown into an article if it's a standalone thing.
- Sometimes I'll recognize a thread as something I've posted about some other time, and mark it as "keep" with the intention of combining it with other threads / seeing what's there.
  - When combining multiple threads into a single article, it's nice to merge the `sources` and `mentions` lists at the top of the markdown file (if you're hosting the articles on the Jekyll site).
- Once an article is written, I move it from `drafts/` to `canon/`.

## the Jekyll site

canonize is designed as a Jekyll site that can be hosted on GitHub Pages.

- Most of the configuration is in `_config.yml` as per normal Jekyll; you should change the values there from  mine to yours.
- `index.md` is the homepage.
- You probably want to delete, or at least completely rewrite `_pages/about.md`.
- The top nav is defined in `_layouts/default.html`, if you want to edit that.

Place articles in either `drafts/` or `canon/`. Articles in `drafts/` will only show up in the explorer if you check the "show drafts" box, and will have a 📝 icon next to them.

The explorer finds these files by checking an index that is generated by running `python gen_contents.py`. This will create a `contents.json` file that you should check in along with your article commits.

## other notes

If you ever re-download your archive, you can update the tweet .js files in `input/` and rerun `tweetpile.py`. It _should_ Just Work, integrating new tweets into their respective conversations. If you have replied to a thread since last time you reviewed it, that thread _should_ show up for review next time you run `twinder.py`. But I haven't tested any of this.

# development TODOs

## next

- [ ] make 404 page a derpy picture of pasha
- [ ] add "random button"

## later

- [ ] add subscribe to feed feature, see [here](https://medium.com/@davideiaiunese/the-problem-why-a-newsletter-baae4409a526) -- needs to come after i've done the first review pass otherwise people will be spammed

## done

- [x] clean up tweets.js into pile
- [x] synthesize tweets into conversations
- [x] TweetDetail graphql for finding missing parents
- [x] fetch tweet context from tweetpile.py
- [x] flatten conversations in depth-first tweet order
- [x] jekyll install + site setup
- [x] jekyll page template
- [x] twinder
- [x] handle reviewed mark
- [x] walk drafts and canon and extract jekyll front matter items
- [x] explorer with filtering etc
- [x] add "show drafts" checkbox to explorer
- [x] write blurb text for home and about pages
- [x] fix date sorting
- [x] GitHub codespaces; install python + ruby devcontainer features
- [x] document the process in this readme
- [x] domain
- [x] render less ugly date in explorer
- [x] cache bust `contents.json` too
- [x] tags at the bottom of pages link you to other pages
- [x] paginate explorer table
- [x] fix description: SEO description should be "from hussein's canon", title bar and header should be "what am i on about?". create "tagline" and replace it where layouts use site.description
- [x] add "hide shitposts" button
- [x] make gen_contents.py a github action instead
- [x] bugfix re deleted accounts 
- [x] automatically create scratch directory if not exists
