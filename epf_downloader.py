# -*- coding: utf-8 -*-

import os
import re
import json
import time
import requests
from requests.auth import HTTPBasicAuth
from BeautifulSoup import BeautifulSoup, SoupStrainer


CONFIG_PATH = "./epf_downloader_config.json"


def _dumpDict(aDict, filePath):
    with open(filePath, mode='w+') as f:
        json.dump(aDict, f, indent=4)


def _loadDict(filePath):
    with open(filePath, mode='r') as f:
        return json.load(f)


class EPFDownloader(object):

    EPF_FILE_PATERN = r'.*\d{8}\.tbz$'
    EPF_DATE_FORMAT = "%d-%b-%Y %H:%M"

    def __init__(self, username, password):
        self.username = username
        self.password = password

        if not os.path.exists(CONFIG_PATH):
            self.options = dict(downloads=[])
            _dumpDict(self.options, CONFIG_PATH)
        else:
            self.options = _loadDict(CONFIG_PATH)

    def perform_download(self):
        raise NotImplementedError()

    def download_files(self):
        self.perform_download()
        _dumpDict(self.options, CONFIG_PATH)

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
