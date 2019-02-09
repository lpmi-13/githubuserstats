import argparse
from github import Github
import json
import yaml
import os
from rateLimit import return_rate_limit

parser = argparse.ArgumentParser()
parser.add_argument('-login', action='store_true')
args = parser.parse_args()

BASE_DIR = './'


def process_issue(issue):
    # first, check if the PR was actually merged
    PR_number = issue.number
    PR_data = issue.repository.get_pull(PR_number)

    if PR_data.merged:
        print('\n\n')
        return issue.html_url, PR_data.merged_at


with open(os.path.join(BASE_DIR, 'config.yaml'), 'r') as GHyaml:
    GHcreds = yaml.load(GHyaml)


if args.login:

    just_logins = ['lpm-13', 'purcell']

else:
    with open(os.path.join(BASE_DIR,
                           'baseline_data',
                           'git-users.json'
                           ),
              'r') as user_file:
        data = json.load(user_file)

    just_logins = [user['login'] for user in data]

g = Github(GHcreds['GITHUB_USERNAME'],
           GHcreds['GITHUB_PASSWORD'],
           timeout=200, per_page=30)

for login in just_logins:

    # so we don't get constant 403's from github
    rate = return_rate_limit(g)
    print('remaining API calls this hour: {}'.format(rate))
    if(rate > 250):

        issues = g.search_issues('type:pr is:merged author:{}'.format(login))
        url_list = []

        for issue in issues:

            print('grabbing {}'.format(issue.html_url))
            issue_rate = return_rate_limit(g)
            print('rate limit count remaining: {}'.format(issue_rate))
            if(rate > 250):

                try:
                    url, date_merged = process_issue(issue)
                    url_list.append({'url': url, 'date_merged': date_merged})
                except:
                    continue
            else:
                print('rate limit too low...waiting...')

        # write to flat file for further analysis by getGraph.py
        with open(os.path.join(BASE_DIR,
                               'data',
                               '{}-results'.format(login)
                               ),
                  'w') as outputfile:
            for url_data in url_list:
                outputfile.write('{},{}'.format(url_data['url'],
                                                url_data['date_merged']
                                                )
                                 )
                outputfile.write('\n')

    else:
        print('rate limit too low...waiting...')
