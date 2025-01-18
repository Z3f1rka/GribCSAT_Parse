#!/usr/bin/env python
# flake8: noqa

import requests

if __name__ == "__main__":
    c = requests.get(
        "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json").json()
    link = ""
    for i in c["channels"]["Stable"]["downloads"]["chromedriver"]:
        if i["platform"] == 'linux64':
            link = i["url"]
    print(link)
