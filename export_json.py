import psycopg2
import json

username = 'postgres'
password = '1341'
database = 'L2'
host = 'localhost'
port = '5432'

OUTPUT_FILE_T = 'lab3_db_{}.csv'

TABLES = [
    'accounts',
    'langs',
    'users',
]

conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)

data = {}
with conn:

    cur = conn.cursor()

    for table in ('accounts', 'langs', 'users'):
        cur.execute('SELECT * FROM ' + table)
        rows = []
        fields = [x[0] for x in cur.description]

    for row in cur:
        rows.append(dict(zip(fields, row)))

    data[table] = rows

    with open('all_data.json', 'w') as outf:
        json.dump(data, outf, default=str)
