#!/usr/bin/env python

"""
Upload HTML files to tenon.io for accessibility scoring.
"""

import argparse
from collections import Counter
import json
import logging
import os
import urlparse

import requests

logging.basicConfig(format="%(levelname)s [%(name)s] %(message)s")
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class Uploader:

    def __init__(self, path, url, key):
        self.path = os.path.realpath(path)
        self.url = url
        self.key = key

    def _save_file(self, filepath):
        """
        Sends the request to tenon.io for the given path to a html file.

        If the requests lib raises an exception, we will leave the file in
        the folder to be retried later. The error will still be logged though.
        These exceptions include:
            * requests.exceptions.ConnectionError
            * requests.exceptions.TooManyRedirects
            * requests.exceptions.Timeout
            * requests.exceptions.HTTPError
            * requests.exceptions.URLRequired

        If any other exception is raised, we will put the file in another
        folder.  It will not be retried, assuming the cause in this case is a
        poorly formatted html file.
        """
        basename = os.path.basename(filepath)

        try:
            with open(filepath) as f:
                data = {'key': self.key, 'src': f.read()}
                resp = requests.post(self.url, data=data)

                # Raise exception if 4XX or 5XX response code is returned
                # The exception raised here will be a subclass or instance
                # of requests.exceptions.RequestException.
                resp.raise_for_status()

                # Raise exception if response code is OK but response
                # text doesn't indicate success. This seems to happen
                # when the file isn't formatted exactly as expected.
                # e.g. 'KeyError: timings'
                # if resp.text != 'Successful':
                #     raise Exception(resp.text)
        except requests.exceptions.RequestException as e:
            log.info("{}: {}".format(basename, e.message))
            return 2
        except Exception as e:
            log.info("{}: {}".format(basename, e.message))
            self._move_file(filepath, 'failed')
            return 1
        else:
            log.info("{}: Successful".format(basename))
            self._move_file(filepath, 'success')
            self._record_results(filepath, resp)
            return 0

    def _move_file(self, filepath, dest):
        base_dir = os.path.dirname(filepath)

        dirs = {
            'failed': os.path.join(base_dir, 'failed_requests'),
            'success': os.path.join(base_dir, 'completed_requests')
        }

        if not os.path.isdir(dirs[dest]):
            os.makedirs(dirs[dest])

        dest = os.path.join(dirs[dest], os.path.basename(filepath))
        # os.rename(filepath, dest)

    def _record_results(self, filepath, response):
        base_dir = os.path.dirname(filepath)
        output_dir = os.path.join(base_dir, 'responses')

        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

        result_file = '{}.txt'.format(os.path.join(output_dir, os.path.basename(filepath)))
        with open(result_file, 'w') as f:
            f.write(response.text)

        result_file = '{}.json'.format(os.path.join(output_dir, os.path.basename(filepath)))
        with open(result_file, 'w') as f:
            f.write(json.dumps(response.json()))


    def upload_htmls(self):
        log.info(
            "Uploading html files from {} to {}".format(self.path, self.url)
        )
        results = Counter()

        if os.path.isfile(self.path):
            results.update([
                self._save_file(self.path)
            ])
        elif os.path.isdir(self.path):
            for f in os.listdir(self.path):
                if f.endswith('.html'):
                    results.update([
                        self._save_file(os.path.join(self.path, f))
                    ])
        else:
            raise Exception(
                "Can't find file or directory {}".format(self.path)
            )

        log.info(
            'Done.'
            '\n{} files successfully uploaded.'
            '\n{} files failed to upload and will not be retried.'
            '\n{} files failed to upload and will be retried next run.'
            ''.format(results[0], results[1], results[2])
        )


def main():
    """
    Runs as standalone script, explicitly passed path to HTML files.

    Args:
        Path to HTML file or directory containing html files to be uploaded.

    Options:
        --key = your tenon.io API key
        --url = URL of tenon API (optional, default: 'https://tenon.io/api/')

    Example:
        python tenon.py test_root/log/auto_screenshots --key MY_API_KEY


    For help text:
        python tenon.py -h
    """
    parser = argparse.ArgumentParser(prog='tenon.py')
    parser.add_argument(
        'htmlpath',
        help=("Path to HTML file or directory containing html files"
              "to be uploaded to the tenon.io api"
              )
    )
    parser.add_argument(
        '--key',
        default='YOUR_KEY_HERE',
        help="tenon.io API key"
    )
    parser.add_argument(
        '--url',
        default='https://tenon.io/api/',
        help="URL of tenon.io API instance (default: 'https://tenon.io/api/')"
    )
    args = parser.parse_args()

    uploader = Uploader(args.htmlpath, args.url, args.key)
    uploader.upload_htmls()


if __name__ == "__main__":
    main()
