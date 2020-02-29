# note: this works for the Events API stuff after 2015

import sys
import os
import hashlib
import json

GITHUB_PR_URL = 'https://github.com'

INPUT_FILE_NAME = sys.argv[1]

INPUT_DIR = 'last_lap_cleaned'
OUTPUT_DIR = 'data'

results_json = []

print('opening {}...'.format(INPUT_FILE_NAME))
with open(os.path.join(INPUT_DIR, '{}'.format(INPUT_FILE_NAME)), 'r') as input_file:
    data = input_file.readlines()

# grab each row and turn the PullRequestEvents into json
formatted = [json.loads(line) for line in data if 'PullRequestEvent' in line]

# iterate through it and check for closed PRs
for item in formatted:
    try:
        repo = item['repo']['name']
        original_owner = repo.split('/')[0]
    except BaseException:
        repo = item['repository']['url']
        original_owner = repo.split('/')[-2]

    try:
        user = item['actor']['login']
    except BaseException:
        user = item['actor_attributes']['login']

    # proceed if the PR was not from the repo owner
    if original_owner != user:

        try:
            if item['payload']['pull_request']['merged']:
                pr_url = item['payload']['pull_request']['html_url']
                created_at = item['created_at']
                hashed_identifier = hashlib.md5('{}:{}'.format(
                    created_at, repo).encode('utf-8')).hexdigest()

                # add this to the results list
                results_json.append(
                    {'UUID': hashed_identifier, 'user': user, 'repo': repo, 'pr_url': pr_url})
        except BaseException:
            print('probably not merged')

print(
    'now trying to write to: {}...'.format(
        os.path.join(
            OUTPUT_DIR,
            'output-{}'.format(INPUT_FILE_NAME))))

with open(os.path.join(OUTPUT_DIR, '{}'.format(INPUT_FILE_NAME)), 'w') as out_file:
    out_file.write(json.dumps(results_json))
