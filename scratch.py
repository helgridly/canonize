import pickle
import os

# create directory called scratch/ if not exists
if not os.path.exists("scratch"):
    os.makedirs("scratch")

def save_reviewed(reviewed):
    with open("scratch/reviewed.pkl", "wb") as f:
        pickle.dump(reviewed, f)


def load_reviewed():
    # if we have a reviewed.pkl file, load it
    try:
        with open("scratch/reviewed.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}


def save_conversations(conversations):
    with open("scratch/conversations.pkl", "wb") as f:
        pickle.dump(conversations, f)


def load_conversations():
    # if we have a conversations.pkl file, load it
    try:
        with open("scratch/conversations.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}


def save_context_pile(context_pile):
    with open("scratch/context_pile.pkl", "wb") as f:
        pickle.dump(context_pile, f)


def load_context_pile():
    # if we have a context_pile.pkl file, load it
    try:
        with open("scratch/context_pile.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}


def save_tweetpile_resume(status_id):
    with open("scratch/tweetpile_resume", "w") as f:
        f.write(status_id)


def load_tweetpile_resume():
    try:
        with open("scratch/tweetpile_resume", "r") as f:
            return f.read()
    except FileNotFoundError:
        return 0