#!/usr/bin/env python3
from feedgen.feed import FeedGenerator
import requests
import sys

def call(startid, direction="later"):
    url = "http://qi.com/call"
    data = {
        "_method"   : "getfeed",
        "_startid"  : startid,
        "_direction": direction,
    }
    r = requests.post(url, data=data)
    feed = r.json()['data']
    if not(feed): feed = []
    return feed

def feed(latest):
    startid = latest
    entries = []
    while True:
        e = call(startid)
        if not(e):
            break

        entries.extend(e)
        startid = max([int(x['id']) for x in e])
    return entries

def build(rss_file, latest):
    fg = FeedGenerator()
    fg.title('QI Feed')
    fg.link(href='qi.com/feed')
    fg.description('Facts from QI')

    maximum = latest
    for e in feed(latest):
        fe = fg.add_entry()
        fe.id(e['id'])
        fe.title(e['title'])
        fe.content(e['body'])
        fe.link(href=e['link'])
        fe.published(e['date'] + ' GMT')

        eid = int(e['id'])
        if eid > maximum:
            maximum = eid

    fg.rss_file(rss_file)
    return maximum

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: {} <output> <latest>".format(sys.argv[0]))
        sys.exit(1)

    rss_file = sys.argv[1]
    latest_file = sys.argv[2]

    latest = int(open(latest_file).read())
    latest = build(rss_file, latest)
    with open(latest_file, 'w') as f:
        f.write(str(latest))

