import psycopg2
import yaml
import json
import os

SRC_DIR = 'data'


def exists_query(name):
    return "select exists ( select 1 from users where username = '{}')".format(
        name)


# get credentials and establish the DB connection
with open('db_config.yaml', 'r') as input_file:
    connection_info = yaml.load(input_file, Loader=yaml.SafeLoader)

con = psycopg2.connect(
    host=connection_info['host'],
    dbname=connection_info['dbname'],
    user=connection_info['user'],
    password=connection_info['password'])

# read in all the json data we collected and parsed
all_files = os.listdir(SRC_DIR)

for json_file in all_files:
    print('opening: {}'.format(json_file))
    with open(os.path.join(SRC_DIR, json_file), 'r') as input_file:
        data = json.load(input_file)

    for item in data:
        cur = con.cursor()
        cur.execute(exists_query(item['user']))
        result = cur.fetchone()[0]
        if not result:
            print('inserting: {}'.format(item['user']))
            cur.execute(
                "INSERT INTO users ( username ) VALUES ('{}')".format(
                    item['user']))
            con.commit()
        cur.execute(
            "INSERT INTO prs (id_user, repo, pr_url) VALUES ((SELECT id FROM users WHERE username = '{}'), '{}', '{}')".format(
                item['user'],
                item['repo'],
                item['pr_url']))
        con.commit()

    os.remove(os.path.join(SRC_DIR, json_file))
con.close()
