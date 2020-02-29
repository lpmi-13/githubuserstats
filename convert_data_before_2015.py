# note: this works for most of the timelineAPI stuff pre-2015

import sys
import os
import hashlib
import json

GITHUB_PR_URL = 'https://github.com'

INPUT_FILE_NAME = sys.argv[1]

INPUT_DIR = 'data'
OUTPUT_DIR = 'cleaned_data'

results_json = []

print('opening {}...'.format(INPUT_FILE_NAME))
with open(os.path.join(INPUT_DIR, '{}'.format(INPUT_FILE_NAME)), 'r') as input_file:
    data = input_file.readlines()

# grab each row and turn the PullRequestEvents into json
formatted = [json.loads(line) for line in data]

# iterate through it and check for closed PRs
for item in formatted:
    try:
        repo = item['repo']['name']
        original_owner = repo.split('/')[0]
    except BaseException:

        try:
            repo = item['repository']['url']
            original_owner = repo.split('/')[-2]

        except BaseException:

            try:
                repo = item['payload']['repo']
                original_owner = repo.split('/')[0]

            except BaseException:
                print('repo still not right')

    try:
        user = item['actor_attributes']['login']
    except BaseException:

        try:
            user = item['actor']

        except BaseException:

            try:
                user = item['actor']['login']
            except BaseException:
                print('user still not right')

    # proceed if the PR was not from the repo owner
    if original_owner != user:

        try:
            if item['payload']['pull_request']['merged']:
                pr_url = item['url']
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
