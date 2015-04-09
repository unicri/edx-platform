"""
API wrapper for tenon.io REST endpoint
"""
class TenonResponse(object):
	"""
	Response from the tenon API
	"""

    def __init__(self, data, response, headers):
        self.response = response
        self.http_headers = headers
        self.json = data

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
