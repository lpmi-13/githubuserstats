from github import Github
import json
import yaml
import os
from rateLimit import return_rate_limit

with open('config.yaml', 'r') as GHyaml:
    GHcreds = yaml.load(GHyaml)

with open(os.path.join('baseline_data', 'git-users.json'), 'r') as user_file:
    data = json.load(user_file)

just_logins = [user['login'] for user in data]

g = Github(GHcreds['GITHUB_USERNAME'], GHcreds['GITHUB_PASSWORD'], timeout=200, per_page=30)

for login in just_logins:

    issues = g.search_issues('author:{} is:pr'.format(login))
    issue_repo_url_list = []
        
    for issue in issues:

        # so we don't get constant 403's from github
        rate = return_rate_limit(g)
        print('remaining API calls this hour: {}'.format(rate))

        if(rate > 250):

            print('grabbing {}'.format(issue.html_url))
    
            try:
                # first, check if the PR was actually merged
                PR_number = issue.number
                PR_data = issue.repository.get_pull(PR_number)
                
                if PR_data.merged:
                    issue_repo_url_list.append([issue.html_url, PR_data.merged_at])
            except:
                continue    

        # write to flat file for further analysis by getGraph.py  
        with open('./data/{}-results'.format(login), 'w') as outputfile:
            for url in issue_repo_url_list:
                outputfile.write(url)
                outputfile.write('\n')
