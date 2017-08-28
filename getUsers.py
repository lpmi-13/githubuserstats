from github import Github
import yaml
import psycopg2
from rateLimit import return_rate_limit
from datetime import datetime

with open('config.yaml', 'r') as GHyamlfile:
    GHcreds = yaml.load(GHyamlfile)

with open('db_config.yaml', 'r') as PGyamlfile:
    PGcreds = yaml.load(PGyamlfile)

#connect to postgres and get the highest user inserted
conn = psycopg2.connect("dbname='github' user='{}' password='{}' host='localhost'".format(PGcreds['username'], PGcreds['password']))
cursor = conn.cursor()

cursor.execute('select UserId from users ORDER BY UserId DESC LIMIT 1;')

user_number = cursor.fetchone()

if (user_number is not None):
    highest_user_id = user_number[0]
else:
    highest_user_id = 0

g = Github(GHcreds['GITHUB_USERNAME'], GHcreds['GITHUB_PASSWORD'], timeout=500, per_page=30)

user_list = g.get_users(since=highest_user_id)

for user in user_list:

    #get the specific user info
    rate = return_rate_limit(g)
    print('rate limit info: {}'.format(rate))
    print('{}'.format(str(datetime.now())))

    if(rate > 4875):
        user = g.get_user(user.login)
    
        #place user info in the DB for later
        cursor.execute('INSERT INTO users (userid, login) VALUES (%s, %s)', (user.id, user.login))
        conn.commit()
        print('inserted entry for user {} into the DB'.format(user.id))
        #get events per user (a merged PR is a type of event in Github)
    #    events = user.get_events()
    #    PR_ids = [event.id for event in events if event == 'PullRequestEvent']
    
        #now loop through all PRs and get the corresponding repo info
        
        #for each repo, check all the issues, and filter by merged
    
        #for all merged issues, if this user has one, increment count in the db
    
conn.close()
