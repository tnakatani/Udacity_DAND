# Joins

## Database Normalization

There are essentially three ideas that are aimed at database normalization [(reference)](https://www.itprotoday.com/microsoft-sql-server/sql-design-why-you-need-database-normalization):

1. Are the tables storing logical groupings of the data?
2. Can I make changes in a single location, rather than in many tables for the same information?
3. Can I access and manipulate data quickly and efficiently?

However, most analysts are working with a database that was already set up with the necessary properties in place. As analysts of data, you don't really need to think too much about data normalization. You just need to be able to pull the data from the database, so you can start drawing insights.

## JOIN

The `JOIN` introduces the second table from which you would like to pull data, and the `ON` tells you how you would like to merge the tables in the `FROM` and `JOIN` statements together.

```sql
SELECT orders.*
FROM orders
JOIN accounts
ON orders.account_id = accounts.id;
```

Above, we are only pulling data from the orders table since in the `SELECT` statement we only reference columns from the orders table

**The `ON` statement links the two tables by a common column.**

### Getting Specific Data

Pull only the account name and the dates in which that account placed an order, but none of the other columns:

```sql
SELECT accounts.name, orders.occurred_at
FROM orders
JOIN accounts
ON orders.account_id = accounts.id;
```

Pull all the columns from both the accounts and orders table.

```sql
SELECT *
FROM orders
JOIN accounts
ON orders.account_id = accounts.id;
```

### JOIN More than Two Tables
![join multiple table](/join_mult_table.png)

```sql
SELECT *
FROM web_events
JOIN accounts
ON web_events.account_id = accounts.id
JOIN orders
ON accounts.id = orders.account_id
```

Or if you want to select specific columns:

```sql
SELECT web_events.channel, accounts.name, orders.total
FROM web_events
JOIN accounts
ON web_events.account_id = accounts.id
JOIN orders
ON accounts.id = orders.account_id
```

## Keys

1. **Primary Key** - A primary key is a unique column in a particular table.  It is common that the primary key is the first column in our tables in most databases.
2. **Foreign Key** - A foreign key is when we see a primary key in another table.

### Primary - Foreign Key Link
![primary foreign diagram](/primary_foreign_key.png)

In the above image you can see that:

1. The `region_id` is the foreign key.
2. The `region_id` is linked to `id` - this is the primary-foreign key link that connects these two tables.
3. The crow's foot shows that the FK can actually appear in many rows in the `sales_reps` table.
4. Single line is telling us that `id` appears only once per row in this table.

## Aliases

```SQL
SELECT *
FROM web_events w -- 'w' is alias for `web_events`
JOIN accounts a -- 'a' is alias for `accounts`
ON w.account_id = a.id -- alias used in place of table name
JOIN orders o
ON a.id = o.account_id
```

---

## JOIN Quiz Pt.1

1. Provide a table for all `web_events` associated with account name of Walmart. There should be three columns. Be sure to include the `primary_poc`, time of the event, and the `channel` for each event. Additionally, you might choose to add a fourth column to assure only Walmart events were chosen.

  ```SQL
  SELECT accounts.primary_poc, web_events.occurred_at,
         web_events.channel, accounts.name
  FROM accounts
  JOIN web_events
  ON accounts.id = web_events.account_id
  WHERE accounts.name LIKE '%Walmart%'
  ```
  *Solution*
  ```SQL
  SELECT a.primary_poc, w.occurred_at, w.channel, a.name
  FROM web_events w
  JOIN accounts a
  ON w.account_id = a.id
  WHERE a.name = 'Walmart';
  ```  

2. Provide a table that provides the region for each `sales_rep` along with their associated accounts. Your final table should include three columns: the region name, the sales rep name, and the account name. Sort the accounts alphabetically (A-Z) according to account name.

  ```SQL
  SELECT region.name AS region,
         sales_reps.name As name,
         accounts.name AS account
  FROM sales_reps
  JOIN accounts
  ON sales_reps.id = accounts.sales_rep_id
  JOIN region
  ON sales_reps.region_id = region.id
  ORDER BY name
  ```

  *Solution*
  ```SQL
  SELECT r.name region, s.name rep, a.name account
  FROM sales_reps s
  JOIN region r
  ON s.region_id = r.id
  JOIN accounts a
  ON a.sales_rep_id = s.id
  ORDER BY a.name;  
  ```

3. Provide the name for each region for every order, as well as the account name and the unit price they paid (total_amt_usd/total) for the order. Your final table should have 3 columns: region name, account name, and unit price. A few accounts have 0 for total, so I divided by (total + 0.01) to assure not dividing by zero.

  ```SQL
  SELECT region.name AS region,
         accounts.name AS account,
         orders.total_amt_usd / (orders.total + 0.01) AS price       
  FROM accounts
  JOIN sales_reps
  ON sales_reps.id = accounts.sales_rep_id
  JOIN region
  ON sales_reps.region_id = region.id
  JOIN orders
  ON accounts.id = orders.account_id
  ```

  *Solution*
  ```SQL
  SELECT r.name region, a.name account,
         o.total_amt_usd/(o.total + 0.01) unit_price
  FROM region r
  JOIN sales_reps s
  ON s.region_id = r.id
  JOIN accounts a
  ON a.sales_rep_id = s.id
  JOIN orders o
  ON o.account_id = a.id;
  ```

---

## LEFT and RIGHT JOINs

`LEFT JOIN` / `RIGHT JOIN` statements pulls all the same rows as an `INNER JOIN`, but they also potentially pull **additional rows**.

If there is not matching information in the JOINed table, then you will have columns with empty cells. These empty cells are called `NULL`.

`LEFT OUTER JOIN` or `RIGHT OUTER JOIN` are exact same commands as `LEFT JOIN` and `RIGHT JOIN`.

##

---

## JOIN Quiz Pt.2
1. Provide a table that provides the region for each `sales_rep` along with their associated accounts. This time only for the Midwest region. Your final table should include three columns: the region name, the sales rep name, and the account name. Sort the accounts alphabetically (A-Z) according to account name.
```SQL
SELECT r.name region, s.name rep, a.name account
FROM sales_reps s
JOIN accounts a
ON s.id = a.sales_rep_id
JOIN region r
ON s.region_id = r.id
WHERE r.id = 2 -- Midwest region ID is 2
ORDER BY rep
```

2. Provide a table that provides the region for each `sales_rep` along with their associated accounts. This time only for accounts where the sales rep has a first name starting with S and in the Midwest region. Your final table should include three columns: the region name, the sales rep name, and the account name. Sort the accounts alphabetically (A-Z) according to account name.
```SQL
SELECT r.name region, s.name rep, a.name account
FROM sales_reps s
JOIN accounts a
ON s.id = a.sales_rep_id
JOIN region r
ON s.region_id = r.id
WHERE r.id = 2 AND s.name LIKE 'S%'
ORDER BY rep
```

3. Provide a table that provides the region for each sales_rep along with their associated accounts. This time only for accounts where the sales rep has a last name starting with K and in the Midwest region. Your final table should include three columns: the region name, the sales rep name, and the account name. Sort the accounts alphabetically (A-Z) according to account name.
```SQL
SELECT r.name region, s.name rep, a.name account
FROM sales_reps s
JOIN accounts a
ON s.id = a.sales_rep_id
JOIN region r
ON s.region_id = r.id
WHERE r.id = 2 AND s.name LIKE '% K%'
ORDER BY rep
```

4. Provide the name for each region for every order, as well as the account name and the unit price they paid (`total_amt_usd`/`total`) for the order. However, you should only provide the results if the standard order quantity exceeds 100. Your final table should have 3 columns: region name, account name, and unit price. In order to avoid a division by zero error, adding .01 to the denominator here is helpful total_amt_usd/(total+0.01).
```SQL
SELECT r.name region, a.name account,
       o.total_amt_usd/(o.total + 0.01) unit_price,
       o.standard_qty as quantity
FROM region r
JOIN sales_reps s
ON s.region_id = r.id
JOIN accounts a
ON a.sales_rep_id = s.id
JOIN orders o
ON o.account_id = a.id
WHERE o.standard_qty > 100
```

5. Provide the name for each region for every order, as well as the account name and the unit price they paid (total_amt_usd/total) for the order. However, you should only provide the results if the standard order quantity exceeds 100 and the poster order quantity exceeds 50. Your final table should have 3 columns: region name, account name, and unit price. Sort for the smallest unit price first. In order to avoid a division by zero error, adding .01 to the denominator here is helpful (total_amt_usd/(total+0.01).
```SQL
SELECT r.name region, a.name account,
       o.total_amt_usd/(o.total + 0.01) unit_price,
       o.standard_qty as quantity,
       o.poster_qty as poster_quantity
FROM region r
JOIN sales_reps s
ON s.region_id = r.id
JOIN accounts a
ON a.sales_rep_id = s.id
JOIN orders o
ON o.account_id = a.id
WHERE o.standard_qty > 100 AND o.poster_qty > 50
ORDER BY unit_price
```

6. Provide the name for each region for every order, as well as the account name and the unit price they paid (total_amt_usd/total) for the order. However, you should only provide the results if the standard order quantity exceeds 100 and the poster order quantity exceeds 50. Your final table should have 3 columns: region name, account name, and unit price. Sort for the largest unit price first. In order to avoid a division by zero error, adding .01 to the denominator here is helpful (total_amt_usd/(total+0.01).
```SQL
SELECT r.name region, a.name account,
       o.total_amt_usd/(o.total + 0.01) unit_price,
       o.standard_qty as quantity,
       o.poster_qty as poster_quantity
FROM region r
JOIN sales_reps s
ON s.region_id = r.id
JOIN accounts a
ON a.sales_rep_id = s.id
JOIN orders o
ON o.account_id = a.id
WHERE o.standard_qty > 100 AND o.poster_qty > 50
ORDER BY unit_price DESC
```

7. What are the different channels used by account id `1001`? Your final table should have only 2 columns: account name and the different channels. You can try SELECT DISTINCT to narrow down the results to only the unique values.
```SQL
SELECT DISTINCT a.name account, w.channel channel
FROM accounts a
JOIN web_events w
ON a.id = w.account_id
WHERE a.id = '1001'
```

8. Find all the orders that occurred in 2015. Your final table should have 4 columns: occurred_at, account name, order total, and order total_amt_usd.
```SQL
SELECT o.occurred_at, a.name, o.total, o.total_amt_usd
FROM accounts a
JOIN orders o
ON o.account_id = a.id
WHERE o.occurred_at BETWEEN '01-01-2015' AND '01-01-2016'
ORDER BY o.occurred_at DESC;
```

---

### Addendum

There are a few more advanced JOINs that we did not cover here, and they are used in very specific use cases. `UNION` and `UNION ALL`, `CROSS JOIN`, and the tricky `SELF JOIN`. These are more advanced than this course will cover, but it is useful to be aware that they exist, as they are useful in special cases.
