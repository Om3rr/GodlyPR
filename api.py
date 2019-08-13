import requests
import shlex
import subprocess
import os
import sys
import json
import re
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
        # uri = os.path.join(base_uri, issue_id, 'assignee')
        #         payload = {"accountId": assign_to}
        #         return sess.request("PUT", url=uri, data=json.dumps(payload))
        r = self.client.request("PUT", self.issue_api(error_id) + "/assignee", data=json.dumps({"accountId": "5b33d3737b8c14625a47f1aa"}))
        r = self.client.request("POST", self.issue_api(error_id) + "/transitions",
                                data=json.dumps({"transition": { "id": '4'}}))
        r = self.client.request("POST", self.issue_api(error_id) + "/transitions",
                                data=json.dumps({"transition": {"id": "721"}}))



    def create_pull_request(self, error_id=None, to_branch=None):
        m = re.search(r"(DEV-\d+)", error_id)
        ticket_id = m.group(1)
        title = self.describe_error(ticket_id)
        self.transit_issue(ticket_id)
        print("hub pull-request -b {0} -h {1} -m '{2}'".format(to_branch, error_id, title))
        print(os.system("hub pull-request -b {0} -h {1} -l \"Ready for Review\" -m \"{2}\"".format(to_branch, error_id, title)))


if __name__ == '__main__':
    try:
        from_branch = sys.argv[1]
        if from_branch == "this":
            from_branch = subprocess.check_output(shlex.split("git rev-parse --abbrev-ref HEAD")).strip().decode('utf-8')
        to_branch = sys.argv[2]
    except:
        from_branch = subprocess.check_output(shlex.split("git rev-parse --abbrev-ref HEAD")).strip().decode('utf-8')
        to_branch = "staging"
    # print
    JiraGodClient().create_pull_request(from_branch, to_branch)
