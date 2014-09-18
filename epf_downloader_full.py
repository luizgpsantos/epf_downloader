# -*- coding: utf-8 -*-

import time
import argparse
from epf_downloader import EPFDownloader


class EPFDowloaderFull(EPFDownloader):

    EPF_FULL_URL = "https://feeds.itunes.apple.com/feeds/epf/v3/full/current/"

    def perform_download(self):
        to_download = set()
        for epf_file_info in self.list_current(self.EPF_FULL_URL):
            epf_file, epf_file_date = epf_file_info

            if not self.options.get(epf_file) or epf_file_date > time.strptime(self.options.get(epf_file), self.EPF_DATE_FORMAT):
                to_download.add(epf_file)
                self.options[epf_file] = time.strftime(self.EPF_DATE_FORMAT, epf_file_date)

        for file_to_download in to_download:
            print "download de %s" % file_to_download


def main():

    parser = argparse.ArgumentParser(description='Import iTunes database into elasticsearch.')
    parser.add_argument('--user', required=True, help='EPF username.')
    parser.add_argument('--password', required=True, help='EPF password.')

    args = parser.parse_args()
    username = args.user
    password = args.password

    EPFDowloaderFull(username=username, password=password).download_files()

if __name__ == "__main__":
    main()
