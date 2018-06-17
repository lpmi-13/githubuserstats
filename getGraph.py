import os
import re

DATA_DIR = './data'
all_files = os.listdir(DATA_DIR)

# used to get the repo owner and repo name from the github URL
git_pattern = re.compile('github.com\/([a-zA-Z0-9-\._]+)\/([a-zA-Z0-9-\._]+)\/')

# used to grab the user name from the flat file we saved earlier in getMerged.py
user_pattern = re.compile('([a-zA-Z0-9-\._]+)-results')

all_users = {}

with open('results.txt', 'w') as outputfile:
    
    for user_file in all_files:
    
        user_match = user_pattern.search(user_file)
        user_name = user_match.group(1)
    
        with open(os.path.join(DATA_DIR, user_file), 'r') as gitfile:
            data = gitfile.read()
        
        all_repos_for_user = []
        
        for repo in data.split('\n'):
            result = git_pattern.search(repo)
            try:
                # if the repo is not owned by the user who authored the PR, then add the repo to our list
                if user_name != result.group(1):
                    all_repos_for_user.append(result.group(2))
            except:
                continue
        
        # get all unique repos that have merged PRs from the user
        unique_repos_to_write = set(all_repos)

        outputfile.write('USER: {}'.format(user_name))

        # put the total unique repos by user into the dictionary
        all_users[user_name] = len(unique_repos_to_write)

        outputfile.write('\n\n')
        
        # write out the list of actual repos since we may want to show it later
        outputfile.write(str(repos_to_write))
        outputfile.write('\n\n')

        # write out the total unique repos as a number
        outputfile.write('number of repos contributed to excluding own: {}'.format(len(repos_to_write)))
        outputfile.write('\n\n')

# sort the ditionary by total unique repos for display later
items = [(v, k) for k, v in all_users.items()]
items.sort()
items.reverse()
items = [(k, v) for v, k in items]
for item in items:
    print(item)
