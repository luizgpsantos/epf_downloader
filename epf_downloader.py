# -*- coding: utf-8 -*-

import os
import re
import json
import time
import requests
from requests.auth import HTTPBasicAuth
from BeautifulSoup import BeautifulSoup, SoupStrainer


def _dumpDict(aDict, filePath):
    with open(filePath, mode='w+') as f:
        json.dump(aDict, f, indent=4)


def _loadDict(filePath):
    with open(filePath, mode='r') as f:
        return json.load(f)


class EPFDownloader(object):

    EPF_FILE_PATERN = r'.*\d{8}\.tbz$'
    EPF_DATE_FORMAT = "%d-%b-%Y %H:%M"

    def __init__(self, username, password, target_dir):
        self.username = username
        self.password = password
        self.target_dir = target_dir
        self.config_path = "%s/epf_downloader_config.json" % self.target_dir

        if not os.path.exists(self.config_path):
            self.options = dict(downloads=[])
            _dumpDict(self.options, self.config_path)
        else:
            self.options = _loadDict(self.config_path)

    def perform_download(self):
        raise NotImplementedError()

    def download_files(self):
        self.perform_download()

    def files_available(self, epf_url):
        directory_list = requests.get(epf_url, auth=HTTPBasicAuth(self.username, self.password)).text
        return self._get_filenames(directory_list)

    def _get_filenames(self, html):
        files = []
        for table_line in BeautifulSoup(html, parseOnlyThese=SoupStrainer('tr')):
            line = table_line.findAll("td")
            if line:
                files.append((line[1].a.get('href'), time.strptime(line[2].text, self.EPF_DATE_FORMAT)))
        return [filename for filename in files if self._match_filename(filename[0])]

    def _match_filename(self, filename):
        pattern = re.compile(self.EPF_FILE_PATERN)
        return pattern.match(filename)
