# -*- coding: utf-8 -*-

import argparse
import epf_downloader
from urlgrabber import urlgrab
from urlgrabber.progress import text_progress_meter


class EPFDowloaderFull(epf_downloader.EPFDownloader):

    EPF_FULL_URL = "https://%s:%s@feeds.itunes.apple.com/feeds/epf/v3/full/current/"

    def perform_download(self):
        to_download = set()
        for epf_file_info in self.files_available(self.EPF_FULL_URL):
            epf_file, epf_file_date = epf_file_info

            if epf_file not in self.options["downloads"]:
                to_download.add(epf_file)

        for file_to_download in to_download:
            print "download de %s" % file_to_download
            try:
                self._download_file(file_to_download)
                self.options["downloads"].append(epf_file)
                epf_downloader._dumpDict(self.options, epf_downloader.CONFIG_PATH)
            except Exception, e:
                print e
                print "erro no download %s" % file_to_download

    def _download_file(self, filename):
        url = "%s%s" % (self.EPF_FULL_URL % (self.username, self.password), filename)
        urlgrab(url, "%s/%s" % (self.target_dir, filename), progress_obj=text_progress_meter(), reget="simple", retry=0)


def main():

    parser = argparse.ArgumentParser(description='Import iTunes database into elasticsearch.')
    parser.add_argument('--user', required=True, help='EPF username.')
    parser.add_argument('--password', required=True, help='EPF password.')
    parser.add_argument('--target_dir', required=True, help='Download target directory.')

    args = parser.parse_args()
    username = args.user
    password = args.password
    target_dir = args.target_dir

    EPFDowloaderFull(username=username, password=password, target_dir=target_dir).download_files()

if __name__ == "__main__":
    main()
