CREATE TABLE items
(
  item_name VARCHAR(30) NOT NULL,
  Product_Price FLOAT,
  PRIMARY KEY (item_name)
);

CREATE TABLE orders
(
  order_number INT NOT NULL,
  order_date DATE,
  PRIMARY KEY (order_number)
);

CREATE TABLE Order_Items
(
  item_name VARCHAR(30) NOT NULL,
  order_number INT NOT NULL,
  quantity INT,
  PRIMARY KEY (item_name, order_number),
  FOREIGN KEY (item_name) REFERENCES items(item_name),
  FOREIGN KEY (order_number) REFERENCES orders(order_number)
);
