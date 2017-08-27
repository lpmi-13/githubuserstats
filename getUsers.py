from github import Github
import os, yaml
import psycopg2

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

g = Github(os.environ['GITHUB_USERNAME'], os.environ['GITHUB_PASSWORD'], timeout=200, per_page=30)

user_list = g.get_users(since=highest_user_id)

for user in user_list:
    #get the specific user info
    user = g.get_user(user.login)

    #place user info in the DB for later
    cursor.execute('INSERT INTO users (userid, login) VALUES (%s, %s)', (user.id, user.login))
    conn.commit()
    print('inserted entry for user {} into the DB'.format(user.id))

conn.close()
