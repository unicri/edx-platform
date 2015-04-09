"""
Upload HTML files to tenon.io for accessibility scoring.
"""
import logging
import requests

log = logging.getLogger(__name__)


class AccessibilityRating:
    """
    A class for sending HTML source to the tenon.io API and determining the accessibility rating.

    Attributes:
        key (str): your tenon.io API key
        url (str): URL of tenon API, defaults to 'https://tenon.io/api/'
    """
    def __init__(self, source, key, url='https://tenon.io/api/'):
        self.url = url
        self.key = key

    def _send_request(self):
        """
        Sends the request to tenon.io for the given html source.
        Returns: response object
        Raises error for 4XX or 5XX response.
        """
        try:
            data = {'key': self.key, 'src': self.source}
            resp = requests.post(self.url, data=data)

            # Raise exception if 4XX or 5XX response code is returned
            resp.raise_for_status()

        except Exception as e:
            log.error(e.message)
            raise

        return resp


class TenonResponse(object):
    """
    A class for parsing the tenon.io API response

    :Args:
        response: The request response object
    """
    def __init__(self, response):
        self.response = response
        self.json = response.json()

    @property
    def api_errors(self):
        return self.json.get('apiErrors')

    @property
    def document_size(self):
        return self.json.get('documentSize')

    @property
    def global_stats(self):
        return self.json.get('globalStats')

    @property
    def message(self):
        return self.json.get('message')

    @property
    def request(self):
        return self.json.get('request')

    @property
    def response_exec_time(self):
        return self.json.get('responseExecTime')

    @property
    def response_time(self):
        return self.json.get('responseTime')

    @property
    def result_set(self):
        return self.json.get('resultSet')

    @property
    def result_summary(self):
        return self.json.get('resultSummary')

    @property
    def source_hash(self):
        return self.json.get('sourceHash')

    @property
    def client_script_errors(self):
        return self.json.get('clientScriptErrors')
