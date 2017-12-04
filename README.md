# HackerNews Reader

This is a simple command line tool to fetch top stories on HackerNews.
It uses the [HackerNews API](https://github.com/HackerNews/API).


## Usage

```
usage: hackernews.py [-h] [--posts N]

optional arguments:
  -h, --help  show this help message and exit
    --posts N   how many posts to print. A positive integer <= 100.

```


## Dependencies

This requires the following to run:
  * Python 3
  * `requests` library:
    * Used to issue HTTP requests to use the HackerNews API.
    * Installation: `python3 -m pip install requests`
  * `rfc3986` library:
    * Used to validate URIs are compliant with RFC 3986.
    * Installation: `python3 -m pip install rfc3986`


## Tests

Tests can be run:
  * Locally, using: `python3 -m unittest`
  * In a Docker container, using: `docker build .`
