# Aggregations

## `NULL`
- NULLs frequently occur when performing a `LEFT` or `RIGHT JOIN`
- NULLs can also occur from simply missing data in our database

## `COUNT`
- `COUNT` can be used on any data type (not just numbers)

Count everything
  ```SQL
  SELECT COUNT(*)
  FROM accounts;
  ```
Count a column
  ```SQL
  SELECT COUNT(accounts.id)
  FROM accounts
  ```

## `SUM`
- Only use on numbers
- Treats `NULL` as zeroes
- Can't use `SUM(\*)`

Compare SUMs
```SQL
SELECT SUM(standard_qty) as standard
       SUM(gloss_qty) as gloss
       SUM(poster_qty) as poster
FROM orders
```

## Quiz Pt.1
1. Find the total amount of `poster_qty` paper ordered in the orders table.
  ```SQL
  SELECT SUM(poster_qty) AS total_poster_sales
  FROM orders
  ```
2. Find the total amount of `standard_qty` paper ordered in the orders table.
  ```SQL
  SELECT SUM(standard_qty) AS total_standard_sales
  FROM orders
  ```
3. Find the total dollar amount of sales using the `total_amt_usd` in the orders table.
  ```SQL
  SELECT SUM(total_amt_usd) AS total_dollar_sales
  FROM orders
  ```
4. Find the total amount spent on `standard_amt_usd` and `gloss_amt_usd` paper for each order in the orders table. This should give a dollar amount for each order in the table.
  ```SQL
  SELECT standard_amt_usd + gloss_amt_usd AS total_standard_gloss
  FROM orders
  ```
5. Find the `standard_amt_usd` per unit of `standard_qty` paper. Your solution should use both an aggregation and a mathematical operator.
  ```SQL
  SELECT SUM(standard_amt_usd) / SUM(standard_qty) AS standard_price_per_unit
  FROM orders
  ```

---

## `MIN` / `MAX` / `AVG` + 'Median'
- Can be used on non-numerical columns
- Ignores `NULL` values
- Depending on the column type, `MIN` will return:
  1. lowest number
  2. earliest date, or
  3. non-numerical value as early in the alphabet as possible
- Depending on the column type, `MIN` will return:
  1. highest number
  2. latest date, or
  3. non-numerical value closest alphabetically to “Z”

MEDIAN - Median happens to be a pretty difficult thing to get using SQL alone — so difficult that finding a median is occasionally asked as an interview question.

## Quiz Pt.2
1. When was the earliest order ever placed? You only need to return the date.
  ```SQL
  SELECT MIN(occurred_at)
  FROM orders
  ```
2. Try performing the same query as in question 1 without using an aggregation function.
  ```SQL
  SELECT occurred_at
  FROM orders
  ORDER BY occurred_at
  LIMIT 1
  ```
3. Find the mean (AVERAGE) amount spent per order on each paper type, as well as the mean amount of each paper type purchased per order.
  ```SQL
  SELECT AVG(standard_qty) AS standard,
  	   AVG(gloss_qty) AS gloss,
         AVG(poster_qty) AS poster,
         AVG(standard_amt_usd) / AVG(standard_qty) AS standard_ppu,
         AVG(gloss_amt_usd) / AVG(gloss_qty) AS gloss_ppu,
         AVG(poster_amt_usd) / AVG(poster_qty) AS poster_ppu       
  FROM orders
  ```
4. What is the MEDIAN `total_usd` spent on all orders?
  ```SQL
  SELECT *
  FROM (SELECT total_amt_usd
        FROM orders
        ORDER BY total_amt_usd
        LIMIT 3457) AS Table1
  ORDER BY total_amt_usd DESC
  LIMIT 2;
  ```
Since there are 6912 orders - we want the average of the 3457 and 3456 order amounts when ordered. This is the average of 2483.16 and 2482.55. This gives the median of 2482.855.

---

## `GROUPBY` Pt.1
- `GROUP BY` can be used to aggregate data within subsets of the data. For example, grouping for different accounts, different regions, or different sales representatives.
- Any column in the `SELECT` statement that is not within an aggregator must be in the `GROUP BY` clause.
- The `GROUP BY` always goes between `WHERE` and `ORDER BY`.
- SQL evaluates the aggregations before the LIMIT clause

## Quiz Pt.3
1. Which account (by name) placed the earliest order? Your solution should have the account name and the date of the order.
  ```SQL
  SELECT a.name AS account,
         o.occurred_at AS order_date
  FROM accounts a
  JOIN orders o
  ON a.id = o.account_id
  ORDER BY order_date
  LIMIT 1
  ```
2. Find the total sales in usd for each account. You should include two columns - the total sales for each company's orders in usd and the company name.
  ```SQL
  SELECT a.name AS company,
	   SUM(o.total_amt_usd) AS total_sales_usd
  FROM accounts a
  JOIN orders o
  ON a.id = o.account_id
  GROUP BY a.name
  ORDER BY a.name
  ```
3. Via what channel did the most recent (latest) web_event occur, which account was associated with this web_event? Your query should return only three values - the date, channel, and account name.
  ```SQL
  SELECT a.name AS account,
         w.channel AS channel,
         w.occurred_at AS date
  FROM accounts a
  JOIN web_events w
  ON a.id = w.account_id
  ORDER BY w.occurred_at DESC
  LIMIT 1
  ```
4. Find the total number of times each type of channel from the web_events was used. Your final table should have two columns - the channel and the number of times the channel was used.
  ```SQL
  SELECT w.channel AS channel,
         COUNT(w.channel) AS count
  FROM web_events w
  GROUP BY w.channel
  ORDER BY w.channel
  ```
5. Who was the primary contact associated with the earliest web_event?
  ```SQL
  SELECT w.occurred_at AS date,
         a.primary_poc AS poc
  FROM web_events w
  JOIN accounts a
  ON a.id = w.account_id
  ORDER BY w.occurred_at
  LIMIT 1
  ```
6. What was the smallest order placed by each account in terms of total usd. Provide only two columns - the account name and the total usd. Order from smallest dollar amounts to largest.
  ```SQL
  SELECT a.name AS account,
         MIN(o.total_amt_usd) AS order_amt
  FROM accounts a
  JOIN orders o
  ON a.id = o.account_id
  GROUP BY a.name
  ORDER BY order_amt
  ```
7. Find the number of sales reps in each region. Your final table should have two columns - the region and the number of sales_reps. Order from fewest reps to most reps.
  ```SQL
  SELECT r.name AS region,
         COUNT(s.region_id) AS rep_count
  FROM region r
  JOIN sales_reps s
  ON r.id = s.region_id
  GROUP BY region
  ORDER BY rep_count
  ```

---

## `GROUPBY` Pt.2
- You can `GROUP BY` multiple columns at once. This is often useful to aggregate across a number of different segments.
  ```SQL
  SELECT account_id, channel, COUNT(id) AS events
  FROM web_events
  GROUP BY account_id, channel -- order doesn't matter
  ORDER BY account_id, channel -- group by account_id first, then channel
  ```
- As with `ORDER BY`, you can substitute numbers for column names in the `GROUP BY` clause. It’s generally recommended to do this only when you’re grouping many columns, or if something else is causing the text in the `GROUP BY` clause to be excessively long.
- A reminder here that any column that is not within an aggregation must show up in your `GROUP BY` statement.

## Quiz Pt. 3
1. For each account, determine the average amount of each type of paper they purchased across their orders. Your result should have four columns - one for the account name and one for the average quantity purchased for each of the paper types for each account.
  ```SQL
  SELECT a.name AS account,
         AVG(standard_amt_usd + gloss_amt_usd + poster_amt_usd) AS order_avg
  FROM accounts a
  JOIN orders o
  ON a.id = o.account_id
  GROUP BY a.name
  ORDER BY a.name
  ```
2. For each account, determine the average amount spent per order on each paper type. Your result should have four columns - one for the account name and one for the average amount spent on each paper type.
  ```SQL
  SELECT a.name AS account,
       AVG(standard_amt_qty) AS standard_avg,
       AVG(gloss_amt_qty) AS gloss_avg,
       AVG(poster_amt_qty) AS poster_avg
  FROM accounts a
  JOIN orders o
  ON a.id = o.account_id
  GROUP BY a.name
  ORDER BY a.name
  ```
3. Determine the number of times a particular channel was used in the web_events table for each sales rep. Your final table should have three columns - the name of the sales rep, the channel, and the number of occurrences. Order your table with the highest number of occurrences first.
  ```SQL
  SELECT s.name AS sales_rep,
         w.channel AS channel,
         COUNT(*) AS channel_count
  FROM web_events w
  JOIN accounts a
  ON w.account_id = a.id
  JOIN sales_reps s
  ON a.sales_rep_id = s.id
  GROUP BY sales_rep, channel
  ORDER BY channel_count DESC
  ```
4. Determine the number of times a particular channel was used in the web_events table for each region. Your final table should have three columns - the region name, the channel, and the number of occurrences. Order your table with the highest number of occurrences first.
  ```SQL
  SELECT r.name AS region,
         w.channel AS channel,
         COUNT(*) AS channel_count
  FROM web_events w
  JOIN accounts a
  ON w.account_id = a.id
  JOIN sales_reps s
  ON a.sales_rep_id = s.id
  JOIN region r
  ON s.region_id = r.id
  GROUP BY region, channel
  ORDER BY channel_count DESC
  ```

---

## `DISTINCT`
- Provides the **unique rows** for all columns written in the `SELECT` statement.
- Always used in `SELECT` statements
- It’s worth noting that using `DISTINCT`, particularly in aggregations, can slow your queries down quite a bit.

Provides the unique rows for all columns written in the `SELECT` statement, e.g.:
```SQL
SELECT DISTINCT column1, column2, column3
FROM table1;
```
Returns the unique (or `DISTINCT`) rows across all three columns.

## Quiz Pt.4
1. Use DISTINCT to test if there are any accounts associated with more than one region.
  ```SQL
  SELECT a.id, r.id, a.name, r.name
  FROM accounts a
  JOIN sales_reps s
  ON a.sales_rep_id = s.id
  JOIN region r
  ON s.region_id = r.id
  ```
  ```SQL
  SELECT DISTINCT id, name
  FROM accounts;  
  ```
  The above two queries have the same number of resulting rows (351), so we know that every account is associated with only one region. If each account was associated with more than one region, the first query should have returned more rows than the second query.

2. Have any sales reps worked on more than one account?
  ```SQL
  SELECT s.id, s.name, COUNT(*) num_accounts
  FROM accounts a
  JOIN sales_reps s
  ON s.id = a.sales_rep_id
  GROUP BY s.id, s.name
  ORDER BY num_accounts;  
  ```
  ```SQL
  SELECT DISTINCT id, name
  FROM sales_reps
  ```
  Actually all of the sales reps have worked on more than one account. The fewest number of accounts any sales rep works on is 3. There are 50 sales reps, and they all have more than one account. Using `DISTINCT` in the second query assures that all of the sales reps are accounted for in the first query.

---  

## `HAVING`
`HAVING` is the “clean” way to filter a query that has been aggregated.

Technical difference between `WHERE` vs `HAVING`:
1. `WHERE` subsets the data based on a logical condition. Doesn't work on aggregations.
2. `HAVING` is like `WHERE`, but works on logical statements involving aggregations.

Keep in mind:
- `WHERE` appear after `FROM`, `JOIN`, and `ON` but before `GROUP BY`
- `HAVING` appear after `GROUP BY` but before `ORDER BY`

```SQL
SELECT account_id,
       SUM(total_amt_usd) AS sum_amt_usd
FROM accounts       
ORDER BY sum_amt_usd
HAVING SUM(total_amt_usd) >= 250000  -- `WHERE` won't work here since it is using an aggregate query:
```

## Quiz Pt.5
1. How many of the sales reps have more than 5 accounts that they manage?
  ```SQL
  SELECT s.name,
         COUNT(*) AS account_num
  FROM sales_reps s
  JOIN accounts a
  ON s.id = a.sales_rep_id
  GROUP BY s.name
  HAVING COUNT(*) > 5
  ORDER BY account_num DESC
  ```   
2. How many accounts spent more than 30,000 usd total across all orders?
  ```SQL
  SELECT a.name account,
         SUM(o.total_amt_usd) total_usd
  FROM accounts a
  JOIN orders o
  ON a.id = o.account_id
  GROUP BY account
  HAVING SUM(o.total_amt_usd) > 30000
  ORDER BY total_usd DESC
  ```
3. Which accounts used facebook as a channel to contact customers more than 6 times?
  ```SQL
  SELECT a.name account,
         COUNT(*) as num_channel
  FROM accounts a
  JOIN web_events w
  ON a.id = w.account_id
  GROUP BY account, w.channel
  HAVING w.channel = 'facebook' AND COUNT(*) > 6
  ORDER BY num_channel DESC
  ```
4. Which account used facebook most as a channel?
  ```SQL
  SELECT a.id, a.name, w.channel, COUNT(*) use_of_channel
  FROM accounts a
  JOIN web_events w
  ON a.id = w.account_id
  WHERE w.channel = 'facebook'
  GROUP BY a.id, a.name, w.channel
  ORDER BY use_of_channel DESC
  LIMIT 1;
  ```
4. Which channel was most frequently used by most accounts?
  ```SQL
  SELECT a.name account,
  	   w.channel as channel,
         COUNT(*) as num_channel
  FROM accounts a
  JOIN web_events w
  ON a.id = w.account_id
  GROUP BY account, channel
  ORDER BY num_channel DESC
  LIMIT 10
  ```
  `DIRECT` is the most frequently used channel.

---

## `DATE` Functions

`DATE_TRUNC` - Truncates date to a particular part of your date-time column. Common trunctions are `day`, `month`, `year`, `dow` (day of week from 0 to 6)
`DATE_PART` - Pulls a specific portion of a date

Query day of week with highest number of orders:
```SQL
SELECT DATE_PART('dow', occurred_at) AS day_of_week
       SUM(total) AS total_qty
FROM orders
GROUP BY 1 -- refers to day_of_week
ORDER BY 2 -- refers to total_qty
```

## Quiz Pt.6
1. Find the sales in terms of total dollars for all orders in each year, ordered from greatest to least.
  ```SQL
  SELECT DATE_PART('year', occurred_at) years,
         SUM(total_amt_usd) AS total_sales
  FROM orders
  GROUP BY 1
  ORDER BY 2 DESC
  ```
2. Which month did Parch & Posey have the greatest sales in terms of total dollars?
  ```SQL
  SELECT DATE_PART('month', occurred_at) months,
         SUM(total_amt_usd) AS total_sales
  FROM orders
  GROUP BY 1
  ORDER BY 2 DESC
  ```
3. Which year did Parch & Posey have the greatest sales in terms of total number of orders?
  ```SQL
  SELECT DATE_PART('month', occurred_at) ord_month, COUNT(*) total_sales
  FROM orders
  WHERE occurred_at BETWEEN '2014-01-01' AND '2017-01-01'
  GROUP BY 1
  ORDER BY 2 DESC;
  ```
4. In which month of which year did Walmart spend the most on gloss paper in terms of dollars?  
  ```SQL
  SELECT a.name account,
         DATE_TRUNC('month', o.occurred_at) months, -- get entire datetime
         SUM(o.gloss_amt_usd) AS gloss_sales
  FROM orders o
  JOIN accounts a
  ON a.id = o.account_id
  GROUP BY 1, 2
  HAVING a.name = 'Walmart'
  ORDER BY 3 DESC
  ```  

---

## `CASE`
- The `CASE` statement always goes in the `SELECT` clause.
- `CASE` must include the following components: `WHEN`, `THEN`, and `END`. `ELSE` is an optional component to catch cases that didn’t meet any of the other previous `CASE` conditions.
- You can make any conditional statement using any conditional operator (like `WHERE`) between `WHEN` and `THEN`. This includes stringing together multiple conditional statements using `AND` and `OR`.
- You can include multiple `WHEN` statements, as well as an `ELSE` statement again, to deal with any unaddressed conditions.

Example: Create a column that divides the `standard_amt_usd` by the `standard_qty` to find the unit price for standard paper for each order.
```SQL
SELECT account_id, CASE WHEN standard_qty = 0 OR standard_qty IS NULL THEN 0
                        ELSE standard_amt_usd/standard_qty END AS unit_price
FROM orders
LIMIT 10;
```

Example: Group `order_count` into tiers.
```SQL
SELECT CASE WHEN total > 500 THEN 'Over 500'
            ELSE '500 or under' END AS total_group
       COUNT(*) AS order_count
FROM orders
GROUP BY 1
```

## Quitz Pt.5
1. We would like to understand 3 different levels of customers based on the amount associated with their purchases. The top branch includes anyone with a Lifetime Value (total sales of all orders) greater than 200,000 usd. The second branch is between 200,000 and 100,000 usd. The lowest branch is anyone under 100,000 usd. Provide a table that includes the level associated with each account. You should provide the account name, the total sales of all orders for the customer, and the level. Order with the top spending customers listed first.
```SQL
SELECT a.name account,
       SUM(o.total_amt_usd) as total_sales,
       CASE WHEN SUM(o.total_amt_usd) > 200000 THEN 'Lifetime Value'
            WHEN SUM(o.total_amt_usd) > 100000 THEN 'Second Tier'
            ELSE 'Third Tier' END AS level
FROM accounts a
JOIN orders o
ON a.id = o.account_id
GROUP BY account
ORDER BY total_sales DESC
```
2. We would now like to perform a similar calculation to the first, but we want to obtain the total amount spent by customers only in 2016 and 2017. Keep the same levels as in the previous question. Order with the top spending customers listed first.
```SQL
SELECT a.name account,
       SUM(o.total_amt_usd) as total_sales,
       CASE WHEN SUM(o.total_amt_usd) > 200000 THEN 'Lifetime Value'
            WHEN SUM(o.total_amt_usd) > 100000 THEN 'Second Tier'
            ELSE 'Third Tier' END AS level,
       DATE_PART('year', o.occurred_at) years
FROM accounts a
JOIN orders o
ON a.id = o.account_id
WHERE o.occurred_at > '2015-12-31'
GROUP BY account, o.occurred_at
ORDER BY total_sales DESC
```
3. We would like to identify top performing sales reps, which are sales reps associated with more than 200 orders. Create a table with the sales rep name, the total number of orders, and a column with top or not depending on if they have more than 200 orders. Place the top sales people first in your final table.
```SQL
SELECT s.name,
       COUNT(*) total_orders,
       CASE WHEN COUNT(*) > 200 THEN 'top'
            ELSE 'not' END AS level
FROM orders o
JOIN accounts a
ON o.account_id = a.id
JOIN sales_reps s
ON a.sales_rep_id = s.id
GROUP BY s.name
ORDER BY total_sales DESC
```
4. The previous didn't account for the middle, nor the dollar amount associated with the sales. Management decides they want to see these characteristics represented as well. We would like to identify top performing sales reps, which are sales reps associated with more than 200 orders or more than 750000 in total sales. The middle group has any rep with more than 150 orders or 500000 in sales. Create a table with the sales rep name, the total number of orders, total sales across all orders, and a column with top, middle, or low depending on this criteria. Place the top sales people based on dollar amount of sales first in your final table. You might see a few upset sales people by this criteria!
```SQL
SELECT s.name,
	   COUNT(*) total_orders,
       SUM(o.total_amt_usd) as total_sales,
       CASE WHEN COUNT(*) > 200 OR SUM(o.total_amt_usd) > 750000 THEN 'top'
            WHEN COUNT(*) > 150 OR SUM(o.total_amt_usd) > 500000 THEN 'middle'
            ELSE 'low' END AS level
FROM orders o
JOIN accounts a
ON o.account_id = a.id
JOIN sales_reps s
ON a.sales_rep_id = s.id
GROUP BY s.name
ORDER BY total_sales DESC
```
