import requests
import os
import sys
import json
class JiraGodClient:
    def __init__(self):
        self.token = os.environ['JIRA_TOKEN']
        self.user = os.environ['JIRA_USER']
        self.cloud_provider = os.environ['JIRA_CLOUD_HOST']
        self.client = self.get_client()

    def issue_api(self, error_id):
        return "https://{0}.atlassian.net/rest/api/3/issue/{1}".format(self.cloud_provider, error_id)

    def get_client(self):
        sess = requests.session()
        sess.headers.update({'Content-Type': 'application/json'})
        sess.auth = (self.user, self.token)
        return sess


    def describe_error(self, error_id):
        issue = self.client.get(self.issue_api(error_id)).json()
        return "{0} - {1}".format(issue['key'], issue['fields']['summary'])


    def transit_issue(self, error_id):
        r = self.client.request("POST", self.issue_api(error_id) + "/transitions",
                                data=json.dumps({"transition": { "id": '4'}}))
        r = self.client.request("POST", self.issue_api(error_id) + "/transitions",
                                data=json.dumps({"transition": {"id": "721"}}))



    def create_pull_request(self, error_id, to_branch):
        title = self.describe_error(error_id)
        print("hub pull-request -b {0} -h {1} -m '{2}'".format(to_branch, error_id, title))
        print(os.system("hub pull-request -b {0} -h {1} -m \"{2}\"".format(to_branch, error_id, title)))
        self.transit_issue(error_id)


if __name__ == '__main__':
    if(len(sys.argv) == 1):
        print("Should run python api.py DEV-1234 branch(optional)")
    try:
        to_branch = sys.argv[2]
    except:
        to_branch = "v2.3"
    # print
    JiraGodClient().create_pull_request(sys.argv[1], to_branch)