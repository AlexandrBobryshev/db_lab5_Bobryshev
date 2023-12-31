import psycopg2
import matplotlib.pyplot as plt

username = 'Bobryshev_Olexandr'
password = '111'
database = 'lab_3_DB'
host = 'localhost'
port = '5432'

'''
Загальна сума продажів кожного товару.
''' 

query_1 = '''
create or replace VIEW TotalItemSales as
	select items.item_name, round(sum(product_price * quantity) :: numeric, 2) as total_sales
	from items
	join order_items on order_items.item_name = items.item_name
	group by items.item_name;
'''


'''
Загальна ціна кожного замовлення.
'''

query_2 = '''
create or replace VIEW TotalOrderPrice as
	select order_items.order_number, round(sum(product_price * quantity) :: numeric, 2) as total_price
	from order_items 
	join items on order_items.item_name = items.item_name
	group by order_items.order_number;
'''

'''
Залежність суми всього замовлення від середньої ціни товару в замовленні.
'''

query_3 = '''
create or replace VIEW OrderStatistics as
	select 
		order_items.order_number, 
		round(avg(items.Product_Price) :: numeric, 2) as average_item_price, 
		round(sum(items.Product_Price * order_items.Quantity) :: numeric, 2) as total_order_price
	from order_items
	join items on order_items .item_name = items.item_name
	group by order_items.order_number
	order by average_item_price;
'''

conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)

with conn:

    cur = conn.cursor()
    cur.execute(query_1)
    cur.execute("select * from TotalItemSales;")
    

    items = []
    total_sales = []

    for row in cur:
        items.append(str(row[0]))
        total_sales.append(round(row[1], 2))
    
    figure, (bar_ax, pie_ax, graph_ax) = plt.subplots(1, 3)
    
    bar = bar_ax.bar(items, total_sales, label='Total', alpha = 0.5)
    bar_ax.bar_label(bar, label_type='center', rotation = 90, fontsize = 10, color = 'red')
    bar_ax.set_title('Загальна ціна кожного замовлення')
    bar_ax.set_xticklabels(items, rotation=30, ha='right', fontsize = 7)  
    bar_ax.set_xlabel('Товар')
    bar_ax.set_ylabel('Сума, $')
    

    cur = conn.cursor()
    cur.execute(query_2)
    cur.execute('select * from TotalOrderPrice;')

    orders = []
    total = []

    for row in cur:
        orders.append(str(row[0]))
        total.append((row[1]))    

    pie_ax.pie(total, labels=orders, autopct='%1.1f%%')
    pie_ax.set_title('Частка кожного замовлення')

    cur.execute(query_3)
    cur.execute('select * from OrderStatistics;')
    
    average_item_price = []
    total_order_price = []

    for row in cur:
        average_item_price.append(row[1])
        total_order_price.append(row[2])

    mark_color = 'blue'
    graph_ax.plot(average_item_price, total_order_price, color=mark_color, marker='o', alpha = 0.5)
    for aip, top in zip(average_item_price, total_order_price):
        graph_ax.annotate(top, xy=(aip, top), color='red',
                        xytext=(4, 7), textcoords='offset points', fontsize=8)
    
    graph_ax.set_xlabel('Середня ціна товару')
    graph_ax.set_ylabel('Ціна замовлення')
    graph_ax.set_title('Залежність суми всього замовлення від середньої ціни товару \nв замовленні.')

figure.subplots_adjust(left=0.1, right=0.9, bottom=0.2, wspace=0.3)
mng = plt.get_current_fig_manager()
mng.resize(1400, 600)
plt.show()