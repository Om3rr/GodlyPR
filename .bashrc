export JIRA_TOKEN=jira_token
export JIRA_CLOUD_HOST=jira_host_name
export JIRA_USER=jira_email

function run_pr {
 python3 /Users/omershacham/PycharmProjects/JiraGod/api.py $1 $2
}
