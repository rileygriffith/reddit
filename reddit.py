#!/usr/bin/env python3

import os
import sys

import requests

# Constants

ISGD_URL = 'http://is.gd/create.php'

# Functions

def usage(status=0):
    ''' Display usage information and exit with specified status '''
    print('''Usage: {} [options] URL_OR_SUBREDDIT

    -s          Shorten URLs using (default: False)
    -n LIMIT    Number of articles to display (default: 10)
    -o ORDERBY  Field to sort articles by (default: score)
    -t TITLELEN Truncate title to specified length (default: 60)
    '''.format(os.path.basename(sys.argv[0])))
    sys.exit(status)

def load_reddit_data(url):
    ''' Load reddit data from specified URL into dictionary

    >>> len(load_reddit_data('https://reddit.com/r/nba/.json'))
    27

    >>> load_reddit_data('linux')[0]['data']['subreddit']
    'linux'
    '''

    if 'https://' in url:
        pass
    else:
        url = 'https://www.reddit.com/r/' + url + '/.json'

    headers = {'user-agent': 'reddit-{}'.format(os.environ.get('USER', 'cse-20289-sp20'))}
    response = requests.get(url, headers=headers)
    data = response.json()['data']['children']

    return data

def shorten_url(url):
    ''' Shorten URL using is.gd service

    >>> shorten_url('https://reddit.com/r/aoe2')
    'https://is.gd/dL5bBZ'

    >>> shorten_url('https://cse.nd.edu')
    'https://is.gd/3gwUc8'
    '''

    r = requests.get(ISGD_URL, params={'format': 'json', 'url': url})
    fields = r.text.split('\"')

    return fields[3]

def print_reddit_data(data, limit=10, orderby='score', titlelen=60, shorten=False):
    ''' Dump reddit data based on specified attributes '''

    if orderby == 'score':
        data = sorted(data, key=lambda p: p['data'][orderby], reverse=True)
    else:
        data = sorted(data, key=lambda p: p['data'][orderby])

    for index, post in enumerate(data[:limit]):
        if index:
            print()

        print(f"{index+1:>4}.\t{post['data']['title'][:titlelen]} (Score: {post['data']['score']})")
        if shorten:
            print(f"\t{shorten_url(post['data']['url'])}")
        else:
            print(f"\t{post['data']['url']}")


def main():
    arguments = sys.argv[1:]
    url       = 'https://www.reddit.com/r/linux/.json'
    limit     = 10
    orderby   = 'score'
    titlelen  = 60
    shorten   = False

    while len(arguments) and arguments[0].startswith('-'):
        argument = arguments.pop(0)
        if argument == '-s':
            shorten = True
        elif argument == '-n':
            limit = int(arguments.pop(0))
        elif argument == '-o':
            orderby = arguments.pop(0)
        elif argument == '-t':
            titlelen = int(arguments.pop(0))
        else:
            usage(1)

    if len(arguments) == 0:
        usage(1)
        
    url = arguments.pop(0)

    data = load_reddit_data(url)

    print_reddit_data(data, limit, orderby, titlelen, shorten)

# Main Execution

if __name__ == '__main__':
    main()

# vim: set sts=4 sw=4 ts=8 expandtab ft=python
