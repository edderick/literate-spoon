#!/usr/bin/python3
"""
This is a utility tool to fetch the latests posts from HackerNews and
output it in a JSON format.
"""

import argparse
import json
import sys

import hnapi


# Maximum number of posts to fetch
MAX_NUM_POSTS = 100


def main():
    """
    Main function:
      - parse command line arguments
      - fetch Hacker News data
      - output in JSON format
    """

    # Parse command line arguments {{{

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--posts',
        metavar='N',
        dest='num_posts',
        type=int,
        help='how many posts to print. A positive integer <= 100.')
    args = parser.parse_args()

    if args.num_posts is None:
        print('Please specify the number of posts to display.',
              file=sys.stderr)
        parser.print_help()
        return 1

    elif args.num_posts <= 0 or args.num_posts > MAX_NUM_POSTS:
        print('Invalid number of posts (0 < N <= {})'.format(MAX_NUM_POSTS),
              file=sys.stderr)
        parser.print_help()
        return 2

    # End of command line parsing }}}

    # Fetch HackerNews stories
    stories = hnapi.get_normalized_top_items(args.num_posts)

    # Output it to JSON
    print(json.dumps(stories, indent=2))


if __name__ == '__main__':
    main()
