# -*- coding: utf-8 -*-

import argparse
from epf_downloader import EPFDownloader


class EPFDowloaderIncremental(EPFDownloader):

    EPF_INCREMENTAL_URL = "https://feeds.itunes.apple.com/feeds/epf/v3/full/current/incremental/"

    def perform_download():
        pass


def main():

    parser = argparse.ArgumentParser(description='Import iTunes database into elasticsearch.')
    parser.add_argument('--user', required=True, help='EPF username.')
    parser.add_argument('--password', required=True, help='EPF password.')

    args = parser.parse_args()
    username = args.user
    password = args.password

    EPFDowloaderIncremental(username=username, password=password).download_files()

if __name__ == "__main__":
    main()
