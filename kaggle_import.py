import csv
import decimal
import psycopg2

username = 'Bobryshev_Olexandr'
password = '111'
database = 'lab_3_DB'

INPUT_CSV_FILE = 'restaurant-1-orders.csv'

delete_query = '''
delete from order_items;
delete from orders;
delete from items;
'''

query_insert_items = '''
INSERT INTO items (item_name, product_price) VALUES (%s, %s)
ON CONFLICT (item_name) DO NOTHING;
'''

query_insert_orders= '''
INSERT INTO orders (order_number, order_date) VALUES (%s, %s)
ON CONFLICT (order_number) DO NOTHING;
'''

query_insert_order_items = '''
INSERT INTO order_items (item_name, order_number, quantity) VALUES (%s, %s, %s);
'''


unique_items = set()
unique_orders = set()

conn = psycopg2.connect(user=username, password=password, dbname=database)

with conn:
    cur = conn.cursor()
    cur.execute(delete_query)

    with open(INPUT_CSV_FILE, 'r') as inf:
        reader = csv.DictReader(inf)
        for i, row in enumerate(reader):
            if i >= 27:
                break
            cur.execute(query_insert_items, (row['Item Name'], row['Product Price']))
            cur.execute(query_insert_orders, (row['Order Number'], row['Order Date']))
            cur.execute(query_insert_order_items, (row['Item Name'], row['Order Number'], row['Quantity']))
        
    conn.commit()