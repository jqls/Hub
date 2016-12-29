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

        if appID == "":
            return False
        # path = "/ws/v1/cluster/apps/" + appID + "/"
        path = "/api/v1/applications/" + appID + "/jobs/"
        info =  json.loads(self.yarn_rest_call(path, "GET")[2])
        print info
        if info == []:
            path = "/api/v1/applications/" + appID
            info = json.loads(self.yarn_rest_call(path, "GET")[2])
            return info['attempts'][0]['completed']
        elif info[0].has_key('status'):
            for i in info:
                if i['status'] != 'SUCCEEDED':
                    return False
            return True
        else:
            return False

    def yarn_rest_call(self, path, action):
        headers = {
            'Accept': 'application/json'
        }
        conn = httplib.HTTPConnection(self.server, self.port)
        conn.request(action, path, '', headers)
        print path
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        conn.close()
        return ret

