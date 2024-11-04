import re
import yaml
import os
import json
import datetime

def extract_front_matter(markdown_filename, draft=False):
    with open(os.path.join("drafts" if draft else "canon", markdown_filename), "r") as f:
        markdown_text = f.read()
    
    # Regular expression to match the front matter block
    front_matter_pattern = re.compile(r'^---\n(.*?)\n---', re.DOTALL | re.MULTILINE)

    # Find the front matter block
    front_matter_match = front_matter_pattern.search(markdown_text)

    if front_matter_match:
        # Extract the front matter YAML data
        front_matter_yaml = front_matter_match.group(1)

        # Parse the YAML data
        front_matter = yaml.safe_load(front_matter_yaml)
        front_matter['path'] = ("drafts" if draft else "canon") + "/" + markdown_filename[:-3]
        front_matter['draft'] = draft
        del front_matter['layout']

        return front_matter
    else:
        return None

def serialize_datetime(obj):
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))

if __name__ == "__main__":
    
    index = []

    for filename in os.listdir("drafts"):
        if filename.endswith(".md"):
            index.append(extract_front_matter(filename, draft=True))
    
    for filename in os.listdir("canon"):
        if filename.endswith(".md"):
            index.append(extract_front_matter(filename, draft=False))
    
    with open("contents.json", "w") as f:
        json.dump(index, f, default=serialize_datetime)
