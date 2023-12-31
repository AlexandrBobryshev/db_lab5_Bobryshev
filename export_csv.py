import csv
import psycopg2

username = 'Bobryshev_Olexandr'
password = '111'
database = 'lab_3_DB'

OUTPUT_FILE = 'lab5_DB_{}.csv'

TABLES = [
    'orders',
    'items',
    'order_items'
]

conn = psycopg2.connect(user=username, password=password, dbname=database)

with conn:
    cur = conn.cursor()

    for table_name in TABLES:

        cur.execute('SELECT * FROM ' + table_name)
        fields = [x[0] for x in cur.description]

        with open(OUTPUT_FILE.format(table_name), 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(fields)
            writer.writerows(cur)
            
