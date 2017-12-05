#!/usr/bin/python3
"""
Wrapper around the HackerNews API.

https://github.com/HackerNews/API
"""

import sys

import requests
from rfc3986 import api, validators, exceptions


# Constants {{{

# Maximum title length
MAX_TITLE_LENGTH = 256

# Maximum username length
MAX_USERNAME_LENGTH = 256

# }}}


# HackerNews API endpoints {{{

# URI to fetch up to 500 top stories
TOP_STORIES_URI = "https://hacker-news.firebaseio.com/v0/topstories.json"

# URI to fetch a particular item
ITEM_URI = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# URI to a HackerNews text story
TEXT_STORY_URL = "https://news.ycombinator.com/item?id={}"

# }}}


def _simple_get_json_request(uri):
    """
    Simple GET request that handles errors in a generic way and
    expects JSON output.
    """
    response = requests.get(uri)
    if response.status_code != 200:
        print("Error (status code: {})  while trying to fetch {}"
              .format(response.status_code, uri),
              file=sys.stderr)
        return None

    try:
        return response.json()
    except ValueError:
        print("Invalid output from {}: Invalid JSON.".format(uri),
              file=sys.stderr)
        return None


def top_stories():
    """
    Get up to 500 top stories IDs.
    """
    stories = _simple_get_json_request(TOP_STORIES_URI)

    return stories if stories is not None else []


def item(news_id):
    """
    Retrieve a HackerNews item given a specific ID.
    """
    return _simple_get_json_request(ITEM_URI.format(news_id))


def get_top_items(num_items):
    """
    Retrieve the details for the N^th top stories.
    """
    return [item(news_id) for news_id in top_stories()[:num_items]]


def get_normalized_top_items(num_items, items=None):
    """
    Retrive the top N^th stories in the following format:

        {
            "title": title,
            "uri": URL,
            "points": points,
            "comments": number of comments,
            "author": author,
            "rank": rank (starting from 1)
        }
    """
    def normalize_news(rank, news):
        """
        Normalize one single news item.
        """

        # Sanitize all inputs; only `id` is guaranteed to be available:
        # https://github.com/HackerNews/API#items
        if "url" in news:
            try:
                validator = validators.Validator().check_validity_of(
                    "scheme",
                    "userinfo",
                    "host",
                    "port",
                    "path",
                    "query",
                    "fragment")
                validator.validate(api.uri_reference(news["url"]))
                url = news["url"]
            except exceptions.InvalidComponentsError:
                url = TEXT_STORY_URL.format(news["id"])
        else:
            url = TEXT_STORY_URL.format(news["id"])

        if "score" in news and news["score"] >= 0:
            score = news["score"]
        else:
            score = 0

        if "descendants" in news and news["descendants"] >= 0:
            comments = news["descendants"]
        else:
            comments = 0

        if "title" in news and len(news["title"]) > 0:
            # Truncate if longer than MAX_TITLE_LENGTH
            title = news["title"][:MAX_TITLE_LENGTH]
        else:
            title = "N/A"

        if "by" in news and len(news["by"]) > 0:
            # Truncate if longer than MAX_USERNAME_LENGTH
            author = news["by"][:MAX_USERNAME_LENGTH]
        else:
            author = "N/A"

        # Return sanitized and normalized entry
        return {
            "title": title,
            "uri": url,
            "points": score,
            "comments": comments,
            "author": author,
            "rank": rank
        }

    if items is None:
        items = get_top_items(num_items)

    return [normalize_news(rank, news)
            for rank, news in enumerate(items[:num_items], start=1)
            if news is not None]
