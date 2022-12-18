import csv
import psycopg2
import matplotlib.pyplot as plt

username = 'postgres'
password = '1341'
database = 'L2'
host = 'localhost'
port = '5432'

INPUT_CSV_FILE = 'Tw_age_gender.csv'
langs = {'en', 'nl', 'fr', 'es', 'pt', 'uk'}

query_d = '''
delete from accounts;
delete from users
'''

query_i = '''
INSERT INTO users VALUES (%s, %s, %s, %s);
INSERT INTO accounts VALUES (%s, %s, %s, %s)
'''

query_1 = '''
drop view if exists time_followers;
Create view time_followers as SELECT acc_age, acc_followers FROM accounts ORDER BY acc_age;
select * from time_followers
'''

query_2 = '''
drop view if exists lang_dist;
Create view lang_dist as SELECT TRIM(lang_name), count(users.user_lang) FROM  users left join langs on users.user_lang=langs.user_lang GROUP BY lang_name;
select * from lang_dist
'''

query_3 = '''
drop view if exists create_age;
Create view create_age as SELECT user_age - acc_age FROM users join accounts on accounts.user_id = users.user_id;
select * from create_age
'''


conn = psycopg2.connect(user = username, password = password, dbname = database, host = host, port = port)

with conn:
    print("Database opened successfully")
    cur = conn.cursor()
    
    cur.execute(query_d)
    with open(INPUT_CSV_FILE, 'r') as inf:
        reader = csv.DictReader(inf, delimiter=',')
        for idx, row in enumerate(reader):
            user_id = idx + 1
            if user_id > 2000:
                break
            user_lang = row['user.lang']
            user_age = row['faceAttributes.age']
            user_gender = row['faceAttributes.gender']
            if user_lang not in langs or user_age == 'NA' or user_gender == 'NA':
                continue
            acc_id = row['index']
            acc_followers = row['user.followers_count']
            acc_age = row['profile_age_y']
            values = (user_id, user_age, user_gender, user_lang, acc_id, acc_followers, acc_age, user_id)
            cur.execute(query_i, values)

    cur.execute(query_1)
    x = []
    y = []
    for row in cur:
        x.append(row[0])
        y.append(row[1])
    plt.bar(x, y, width=0.1)
    plt.title("time - followers correlation")
    plt.xlabel("account age")
    plt.ylabel("followers count")
    plt.show()

    x = []
    y = []
    t = 0
    cur.execute(query_2)
    for row in cur:
        x.append(row[0])
        y.append(row[1])
        t += y[-1]
    for i in range(len(x)):
        x[i] = x[i] + "({}%)".format(round((100*y[i]/t),2))
    plt.pie(y, labels=x)
    plt.title("user language distribution")
    plt.show()

    x = []
    cur.execute(query_3)
    for row in cur:
        x.append(row[0])
    plt.bar(range(len(x)) ,x)
    plt.title("user age at the moment of creating account")
    plt.xlabel("user id")
    plt.ylabel("age")
    plt.show()

