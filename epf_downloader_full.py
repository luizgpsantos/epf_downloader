# -*- coding: utf-8 -*-

import argparse
from epf_downloader import EPFDownloader
from urlgrabber import urlgrab
from urlgrabber.progress import text_progress_meter


class EPFDowloaderFull(EPFDownloader):

    EPF_FULL_URL = "https://%s:%s@feeds.itunes.apple.com/feeds/epf/v3/full/current/"

    def perform_download(self):
        to_download = set()
        for epf_file_info in self.files_available(self.EPF_FULL_URL):
            epf_file, epf_file_date = epf_file_info

            if epf_file not in self.options["downloads"]:
                to_download.add(epf_file)
                self.options["downloads"].append(epf_file)

        for file_to_download in to_download:
            print "download de %s" % file_to_download
            self._download_file(file_to_download)

    def _download_file(self, filename):
        url = "%s%s" % (self.EPF_FULL_URL % (self.username, self.password), filename)
        urlgrab(url, filename, progress_obj=text_progress_meter())


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
