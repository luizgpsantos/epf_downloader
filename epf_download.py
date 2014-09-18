# -*- coding: utf-8 -*-

import re
import argparse
import requests
from requests.auth import HTTPBasicAuth
from BeautifulSoup import BeautifulSoup, SoupStrainer


class EPFDownloader(object):

    EPF_URL = "https://feeds.itunes.apple.com/feeds/epf/v3/full/current/"
    FILE_PATERN = r'.*\d{8}\.tbz$'

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def list_current(self):
        directory_list = requests.get(self.EPF_URL, auth=HTTPBasicAuth(self.username, self.password)).text
        print self.get_filenames(directory_list)

    def get_filenames(self, html):
        filenames = []
        for filename in BeautifulSoup(html, parseOnlyThese=SoupStrainer('a')):
            filenames.append(filename.get('href'))
        return [filename for filename in filenames if self._match_filename(filename)]

    def _match_filename(self, filename):
        pattern = re.compile(self.FILE_PATERN)
        return pattern.match(filename)


def main():

    parser = argparse.ArgumentParser(description='Import iTunes database into elasticsearch.')
    parser.add_argument('--user', required=True, help='EPF username.')
    parser.add_argument('--password', required=True, help='EPF password.')

    args = parser.parse_args()
    username = args.user
    password = args.password

    EPFDownloader(username=username, password=password).list_current()

if __name__ == "__main__":
    main()
