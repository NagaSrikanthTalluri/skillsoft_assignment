from github import Github
from datetime import datetime
import json
import requests
import os

slack_data = {
        "username": "NotificationBot",
        "icon_emoji": ":satellite:",
        "attachments": [
            {
                "color": "",
                "fields": [
                    {
                        "title": "PR to be reviewed",
                        "value": "PR to be reviewed",
                        "short": "false",
                    }
                ]
            }
        ]
    }


def push_pr_to_slack():
    cur_day = datetime.now().strftime("%d")
    cut_off_day = int(cur_day) - 3
    g = Github()
    repo_name = os.getenv("REPO_NAME", "skillsoft_assignment")
    user = g.get_user(os.getenv("GIT_USERNAME", "TejaNagaSrikanth"))
    slack_url = os.getenv("SLACK_URL", "https://hooks.slack.com/services/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")
    for repo in user.get_repos():
        if repo_name is not None and repo.full_name.endswith(repo_name):
            pr_list = repo.get_pulls()
            if not pr_list:
                continue
            while True:
                import time
                time.sleep(int(os.getenv("INTERVAL", 300)))
                for pr in pr_list:
                    if pr.created_at.day in range(int(cut_off_day), int(cur_day) + 1):
                        slack_data["attachments"][0]["color"] = "#008000"
                        slack_data["attachments"][0]["fields"][0]["value"] = pr.title + " " + pr.url
                        requests.post(url=slack_url, data=json.dumps(slack_data))
                    else:
                        slack_data["attachments"][0]["color"] = "#FF0000"
                        requests.post(url=slack_url, data=json.dumps(slack_data))
    return

if __name__ == '__main__':
    push_pr_to_slack()


