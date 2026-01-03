1. ------------------------------Entity relationship Description ----------------------------
#Database schema documentation - Fleximart

This document describes the **relational database schema** used in the FlexiMart ETL pipeline.
It includes entity descriptions, attributes, and relationships between tables.

1. Entity- Customers

Stores customer related information for users who place orders in fleximart

Attributes ->
     a. customer_id - unique identifier for each customer
     b. first_name - customer first name
     c. customer last name
     d. email - customer email address (unique value)
     e. phone - customer phone number 
     f. city - city where customer resides 
     g. registration_date - customer registration date

Relationship -> one customer can place multiple orders

2. Entity - Products

Stores product details available for sales in fleximart store

Attributes ->

     a. product_id - unique identifier for each product
     b. product_name - name of the product
     c. category - category to which the product belongs
     d. price - unit price of the product
     e. stock_quantity - available quantity

Relationship -> one product can appear in many orders

3. Entity - Orders

Stores order-level information for each purchase made by a customer

Attributes -> 
     a. order_id - unique identifier for each product 
     b. customer_id - identifier of the customer who has placed an order
     c. order_date - date when order is placed
     d. total_amount - total value of the order
     e. status - current status of the order (i.e. pending, completed, cancelled)

Relationship -> one customer can place many orders

4. Entity - order_items

Stores item-level details for each order

Attributes ->
     a. order_item_id - unique identifier for each order item
     b. order_id - identifier of the related order
     c. product_id - identifier of the product purchased 
     d. quantity - number of units purchased
     e. unit_price - price per unit at the time of purchase 
     f. subtotal - total price of the item (quantity * unit_price)

Relationship -> order items belong to one order 

This schema supports efficient storage, querying, and analysis of customer orders and product sales data.

2. --------------------------------Normalization Explanation----------------------------------------

The FlexiMart database schema is designed in Third Normal Form (3NF) to ensure data integrity, eliminate redundancy, and avoid common data anomalies.

Functional Dependencies ->

Each table in the schema has a clearly defined primary key, and all non-key attributes are fully functionally dependent on that key:

     customers ->
          customer_id → first_name, last_name, email, phone, city, registration_date

     products -> 
          product_id → product_name, category, price, stock_quantity

     orders -> 
          order_id → customer_id, order_date, total_amount, status

     order_items -> 
          order_item_id → order_id, product_id, quantity, unit_price, subtotal

There are no partial dependencies because each table uses a single-column primary key. There are also no transitive dependencies, as non-key attributes do not depend on other non-key attributes.

Why the Design is in 3NF
     A table is in 3NF if:
          1. It is in Second Normal Form (2NF), and
          2. No non-key attribute depends on another non-key attribute.

     This design satisfies both conditions:
          a. Customer information is stored only in the customers table.
          b. Product information is stored only in the products table.
          c. Order and item details are separated into orders and order_items.

Overall, the schema ensures data consistency, scalability, and maintainability, which are key objectives of 3NF design.

3. --------------------------Sample Data Representation-------------------------------

This section presents sample records from each table to illustrate how data is stored after the ETL process.

Table : Customers

| customer_id | first_name | last_name | email |   phone   | City registration_date |               
| ----------: | ---------- | --------- | --------|---------|------------------------|
|           1 | Rahul | Sharma | [rahul.sharma@gmail.com]| +91-9876543210 | Bangalore | 2023-01-15
|           2 | Priya | Patel  | [priya.patel@yahoo.com] | +91-9988776655 | Mumbai    | 2023-02-20  
|           3 | Amit  | Kumar  | [amit.kumar@gmail.com]  | +91-9765432109 | Delhi     | 2023-03-10 


Table : Products

| product_id | product_name       | category    | price | stock_quantity |
| ---------: | ------------------ | ----------- | ----- | -------------- |
|          1 | Samsung Galaxy S21 | Electronics | 45999 | 150            |
|          2 | Nike Running Shoes | Fashion     | 3499  | 80             |
|          3 | Organic Almonds    | Groceries   | 899   | 200            |


Table : Orders

| order_id | customer_id | order_date | total_amount | status    |
| -------: | ----------: | ---------- | ------------ | --------- |
|        1 |           1 | 2024-01-15 | 45999        | Completed |
|        2 |           2 | 2024-01-16 | 5998         | Completed |
|        3 |           3 | 2024-01-20 | 1950         | Pending   |


Table : order_items

| order_item_id | order_id | product_id | quantity | unit_price | subtotal |
| ------------: | -------: | ---------: | -------: | ---------: | -------: |
|             1 |        1 |          1 |        1 |      45999 |    45999 |
|             2 |        2 |          2 |        2 |       2999 |     5998 |
|             3 |        3 |          3 |        2 |        975 |     1950 |


