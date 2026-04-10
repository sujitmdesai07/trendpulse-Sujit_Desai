# TrendPulse_collector.py
# Collect trending Hacker News stories, classify them, and store in JSON

#Import essential libraries-----

import requests
import time
import os
import json

from datetime import datetime

#Given Configuration----------

headers = {"User-Agent": "TrendPulse/1.0"}

categories = {
    "technology": ["tech", "software", "app"],
    "entertainment": ["movie", "music", "film"],
    "AI": ["ai", "machine learning", "chatgpt"],
    "programming": ["python", "javascript", "coding"],
    "science": ["science", "research", "space"]
}

#Fetch first 500 stories data--------

def get_top_ids():
    print("Fetching top story IDs...")

    try:
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        res = requests.get(url, headers=headers)

        if res.status_code == 200:
            ids = res.json()[:500]
            print(f"  Retrieved {len(ids)} total IDs. Using first 500.\n")
            return ids
        else:
            print("Failed to fetch IDs")
            return []

    except:
        print("Error fetching IDs")
        return []


#Fetch each story data-------

def get_story(story_id):
    try:
        url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        res = requests.get(url, headers=headers)

        if res.status_code != 200:
            print(f"  Failed story {story_id}")
            return None

        return res.json()

    except:
        print(f"  Error story {story_id}")
        return None


def match_category(title, words):
    title = title.lower()
    return any(w in title for w in words)


#Story Collection-----

def collect_stories(ids):
    print("Collecting stories...\n")

    results = []
    counts = {cat: 0 for cat in categories}

    for cat, words in categories.items():

        for i in ids:
            if counts[cat] >= 25:
                break

            s = get_story(i)
            if not s or "title" not in s:
                continue

            if not match_category(s["title"], words):
                continue

            results.append({
                "post_id": s.get("id"),
                "title": s.get("title"),
                "category": cat,
                "score": s.get("score", 0),
                "num_comments": s.get("descendants", 0),
                "author": s.get("by"),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            counts[cat] += 1

        print(f"  Category '{cat}' full ({counts[cat]} stories). Sleeping 2s...")
        time.sleep(2)

    return results


# Save JSON file in Data-------

def save_data(data):
    os.makedirs("data", exist_ok=True)
    fname = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(fname, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"\nCollected {len(data)} stories. Saved to {os.path.abspath(fname)}")


# Actual Run----

ids = get_top_ids()
stories = collect_stories(ids)
save_data(stories)
