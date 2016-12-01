import httplib
import json

class SparkMonitor:

    def __init__(self, server, port):
        self.server = server
        self.port = port

    def byteify(self, input):
        if isinstance(input, dict):
            return {self.byteify(key): self.byteify(value) for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [self.byteify(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input

    def appInfo(self, appID):
        path = "/ws/v1/cluster/apps/" + appID + "/"
        return self.yarn_rest_call(path, "GET")

    def yarn_rest_call(self, path, action):
        headers = {
            'Accept': 'application/json'
        }
        conn = httplib.HTTPConnection(self.server, self.port)
        conn.request(action, path, '', headers)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        conn.close()
        return ret