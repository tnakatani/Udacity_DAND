# `Subqueries`

Example:  Find the average number of events for each day for each channel. The first table will provide us the number of events for each day and channel, and then we will need to average these values together using a second query.

```SQL
SELECT channel,
       AVG(event_count) as avg_per_day
FROM (SELECT DATE_TRUNC('day', occurred_at) AS day, -- subquery
             channel,
             COUNT(*) as event_count
      FROM web_events
      GROUP BY 1, 2
      ORDER BY 3 desc) sub -- end subquery, need alias
GROUP BY channel
ORDER BY 2 DESC
```

In the first subquery, it queried a table to be queried again in the `FROM` statement. However, if you are only returning a single value, you might use that value in a logical statement like `WHERE`, `HAVING`, or even `SELECT` - the value could be nested within a `CASE` statement.

```SQL
SELECT *
FROM orders
WHERE DATE_TRUNC('month', occurred_at) =
  (SELECT DATE_TRUNC('month', MIN(occured_at)) AS min_month
   FROM orders)
ORDER BY occurred_at
```

  - Note that you should not include an alias when you write a subquery in a conditional statement. This is because the subquery is treated as an individual value (or set of values in the `IN` case) rather than as a table.
  - Also, notice the query here compared a single value. If we returned an entire column `IN` would need to be used to perform a logical argument. If we are returning an entire table, then we must use an `ALIAS` for the table, and perform additional logic on the entire table.

Find all orders that took place in the first month & year as the first order, then pull the average for each paper type.
```SQL
SELECT AVG(standard_qty) standard_avg,
       AVG(gloss_qty) gloss_avg,
       AVG(poster_qty) poster_avg
FROM orders
WHERE DATE_TRUNC('month', occurred_at) =
  (SELECT DATE_TRUNC('month', MIN(occurred_at))
  FROM orders)
```

## Quiz Pt.1
**Q1: Provide the name of the sales_rep in each region with the largest amount of total_amt_usd sales.**

Step 1: Find the `total_amt_usd` totals associated with each sales rep, and the region in which they were located.
```SQL
SELECT s.name AS sales_rep,
       r.name AS region,
       SUM(o.total_amt_usd) AS total_sales
FROM sales_reps s
JOIN accounts a
ON s.id = a.sales_rep_id
JOIN region r
ON s.region_id = r.id
JOIN orders o
ON a.id = o.account_id
GROUP BY 1, 2
ORDER BY 3 DESC
```
Step 2: Find the maximum total sales for each region.
```SQL
SELECT region,
       MAX(total_sales) total_sales
FROM (SELECT s.name AS sales_rep,
             r.name AS region,
             SUM(o.total_amt_usd) AS total_sales
         FROM sales_reps s
         JOIN accounts a
         ON s.id = a.sales_rep_id
         JOIN region r
         ON s.region_id = r.id
         JOIN orders o
         ON a.id = o.account_id
         GROUP BY 1, 2) t1
GROUP BY 1
```
Step 3: `JOIN` the two tables
```SQL
SELECT t3.rep_name, t3.region_name, t3.total_amt
FROM(SELECT region_name, MAX(total_amt) total_amt
     FROM(SELECT s.name rep_name, r.name region_name, SUM(o.total_amt_usd) total_amt
          FROM sales_reps s
          JOIN accounts a
          ON a.sales_rep_id = s.id
          JOIN orders o
          ON o.account_id = a.id
          JOIN region r
          ON r.id = s.region_id
          GROUP BY 1, 2) t1
          GROUP BY 1) t2
JOIN(SELECT s.name rep_name, r.name region_name, SUM(o.total_amt_usd) total_amt
     FROM sales_reps s
     JOIN accounts a
     ON a.sales_rep_id = s.id
     JOIN orders o
     ON o.account_id = a.id
     JOIN region r
     ON r.id = s.region_id
     GROUP BY 1,2
     ORDER BY 3 DESC) t3
ON t3.region_name = t2.region_name AND t3.total_amt = t2.total_amt;
```

**Q2: For the region with the largest (sum) of sales total_amt_usd, how many total (count) orders were placed?**

Step 1: Pull total sales for each region.
```SQL
SELECT r.name region_name, SUM(o.total_amt_usd) total_amt
FROM sales_reps s
JOIN accounts a
ON a.sales_rep_id = s.id
JOIN orders o
ON o.account_id = a.id
JOIN region r
ON r.id = s.region_id
GROUP BY r.name
```
Step 2: Pull region with highest sum of sales.
```SQL
SELECT MAX(total_amt)
FROM (SELECT r.name region_name, SUM(o.total_amt_usd) total_amt
      FROM sales_reps s
      JOIN accounts a
      ON a.sales_rep_id = s.id
      JOIN orders o
      ON o.account_id = a.id
      JOIN region r
      ON r.id = s.region_id
      GROUP BY r.name) t1
```
Step 3: Pull the total orders for the region
```SQL
SELECT r.name region,
       COUNT(o.total) total_orders
FROM sales_reps s
JOIN accounts a
ON a.sales_rep_id = s.id
JOIN orders o
ON o.account_id = a.id
JOIN region r
ON r.id = s.region_id
GROUP BY r.name
HAVING SUM(o.total_amt_usd) = (
  SELECT MAX(total_amt)
  FROM (SELECT r.name region_name, SUM(o.total_amt_usd) total_amt
        FROM sales_reps s
        JOIN accounts a
        ON a.sales_rep_id = s.id
        JOIN orders o
        ON o.account_id = a.id
        JOIN region r
        ON r.id = s.region_id
        GROUP BY r.name) sub);
```
**Q3: For the account that purchased the most (in total over their lifetime as a customer) `standard_qty` paper, how many accounts still had more in total purchases?**

Step 1: Find the account that purchased the most `standard_qty` paper.
```SQL
SELECT a.name AS account,
       SUM(o.standard_qty) AS standard_sum,
       SUM(o.total) AS total_sum
FROM accounts a
JOIN orders o
ON a.id = o.account_id
GROUP BY 1
```
Step 2: Pull accounts with greater total orders than max `standard_qty` purchase.
```SQL
SELECT a.name account
FROM accounts a
JOIN orders o
ON a.id = o.account_id
GROUP BY 1
HAVING SUM(o.total) > (SELECT total
                  FROM (SELECT a.name act_name, SUM(o.standard_qty) tot_std, SUM(o.total) total
                        FROM accounts a
                        JOIN orders o
                        ON o.account_id = a.id
                        GROUP BY 1
                        ORDER BY 2 DESC
                        LIMIT 1) sub);                
```
**Q4: For the customer that spent the most (in total over their lifetime as a customer) `total_amt_usd`, how many `web_events` did they have for each channel?**
Step 1: Find account that spent the most `total_amt_usd`
```SQL
SELECT a.id id, a.name account, SUM(o.total_amt_usd) total_amt
FROM accounts a
JOIN orders o
ON a.id = o.account_id
GROUP BY 1, 2
ORDER BY 3 DESC
LIMIT 1
```
Step 2: Find how many `web_events` they had for each channel.
```SQL
SELECT a.id id, a.name account, w.channel, COUNT(*) as event_count
FROM web_events w
JOIN accounts a
ON a.id = w.account_id
GROUP BY 1, 2, 3
ORDER BY 4 DESC
```
Step 3: Combine queries
```SQL
SELECT a.name account, w.channel, COUNT(*) as event_count
FROM web_events w
JOIN accounts a
ON a.id = w.account_id
WHERE a.id = (SELECT id
              FROM (SELECT a.id id, a.name account, SUM(o.total_amt_usd) total_amt
                    FROM accounts a
                    JOIN orders o
                    ON a.id = o.account_id
                    GROUP BY 1, 2
                    ORDER BY 3 DESC
                    LIMIT 1)sub)
GROUP BY 1, 2
ORDER BY 3 DESC
```

**Q5: What is the lifetime average amount spent in terms of `total_amt_usd` for the top 10 total spending accounts?**
Step 1: Find lifetime avg amount spent for top 10 accounts.
```SQL
SELECT a.id id, a.name account, SUM(total_amt_usd) AS total_amt_sum
FROM accounts a
JOIN orders o
ON a.id = o.account_id
GROUP BY 1, 2
ORDER BY 3 DESC
LIMIT 10
```
Step 2: Find average amount spent from top 10
```SQL
SELECT sub.account, AVG(sub.total_amt_sum) AS avg_amt
FROM (SELECT a.id id, a.name account, SUM(total_amt_usd) AS total_amt_sum
      FROM accounts a
      JOIN orders o
      ON a.id = o.account_id
      GROUP BY 1, 2
      ORDER BY 3 DESC
      LIMIT 10) sub
GROUP BY 1
ORDER BY avg_amt DESC
```

**Q6: What is the lifetime average amount spent in terms of `total_amt_usd` for only the companies that spent more than the average of all orders.**

Step 1: Pull the average of all accounts in terms of `total_amt_usd`.
```SQL
SELECT AVG(o.total_amt_usd) avg_all
FROM orders o
JOIN accounts a
ON a.id = o.account_id;
```

Step 2: Only pull the accounts with more than this average amount.
```SQL
SELECT o.account_id, AVG(o.total_amt_usd) avg_amt
FROM orders o
GROUP BY 1
HAVING AVG(o.total_amt_usd) > (SELECT AVG(o.total_amt_usd) avg_all
                               FROM orders o
                               JOIN accounts a
                               ON a.id = o.account_id)            
```

Step 3: Get the average of `total_amt_usd` from all accounts.
```SQL
SELECT AVG(avg_amt)
FROM (SELECT o.account_id, AVG(o.total_amt_usd) avg_amt
      FROM orders o
      GROUP BY 1
      HAVING AVG(o.total_amt_usd) > (SELECT AVG(o.total_amt_usd) avg_all
                                     FROM orders o
                                     JOIN accounts a
                                     ON a.id = o.account_id)) sub
```

## `WITH`

`WITH` can be thought of as a more efficient version of a subquery.

Example: Find the average number of events for each channel per day.

1. Using a subquery:
  ```SQL
  SELECT channel, AVG(events) AS average_events
  FROM (SELECT DATE_TRUNC('day',occurred_at) AS day, channel, COUNT(*) as events
           FROM web_events
           GROUP BY 1,2) sub
  GROUP BY channel
  ORDER BY 2 DESC;
  ```

2. Move the subquery into its own table using `WITH` with an `alias` named `events`. Reference it using another query.

  ```SQL
  WITH events AS (SELECT DATE_TRUNC('day',occurred_at) AS day, channel, COUNT(*) as events
                  FROM web_events
                  GROUP BY 1,2)

  SELECT channel, AVG(events) AS average_events
  FROM events
  GROUP BY channel,
  ORDER BY 2 DESC
  ```

- More than one table can be created in a `WITH` statement.

  ```SQL
  WITH table1 AS (
            SELECT *
            FROM web_events),

       table2 AS (
            SELECT *
            FROM accounts)

  SELECT *
  FROM table1
  JOIN table2
  ON table1.account_id = table2.id;          
  ```

## Quiz

**1. Provide the name of the `sales_rep` in each region with the largest amount of `total_amt_usd` sales.**
```SQL
WITH t1 AS (
  SELECT s.name rep_name, r.name region_name, SUM(o.total_amt_usd) total_amt
  FROM sales_reps s
  JOIN region r
  ON s.region_id = r.id
  JOIN accounts a
  ON a.sales_rep_id = s.id
  JOIN orders o
  ON o.account_id = a.id
  GROUP BY rep_name, region_name),
t2 AS (
  SELECT region_name, MAX(total_amt) total_amt
  FROM t1
  GROUP BY region_name
  )

SELECT t1.rep_name, t1.region_name, t1.total_amt
FROM t1
JOIN t2
ON t1.region_name = t2.region_name AND t1.total_amt = t2.total_amt
ORDER BY total_amt DESC
```

**2. For the `region` with the largest sales `total_amt_usd`, how many total orders were placed?**
```SQL
WITH t1 AS (
  SELECT r.name region_name, MAX(o.total_amt_usd) total_amt
  FROM region r
  JOIN sales_reps s
  ON r.id = s.region_id
  JOIN accounts a
  ON a.sales_rep_id = s.id
  JOIN orders o
  ON o.account_id = a.id  
  GROUP BY region_name, o.total
  ORDER BY total_amt DESC
  LIMIT 1
),
t2 AS (
  SELECT r.name region_name, COUNT(o.total) total_order
  FROM region r
  JOIN sales_reps s
  ON r.id = s.region_id
  JOIN accounts a
  ON a.sales_rep_id = s.id
  JOIN orders o
  ON o.account_id = a.id
  GROUP BY region_name
)

SELECT t1.region_name, t2.total_order
FROM t1
JOIN t2
ON t1.region_name = t2.region_name
```

**3. For the name of the account that purchased the most (in total over their lifetime as a customer) standard_qty paper, how many accounts still had more in total purchases?**
```SQL
WITH t1 AS (
  SELECT a.name account, SUM(o.standard_qty) total_std_order
  FROM accounts a
  JOIN orders o
  ON o.account_id = a.id
  GROUP BY account
  ORDER BY total_std_order DESC
  LIMIT 1
),
t2 AS (
  SELECT a.name account, SUM(o.total) total_qty
  FROM accounts a
  JOIN orders o
  ON o.account_id = a.id
  GROUP BY account
  HAVING SUM(o.total) > (SELECT total_std_order FROM t1)
)
SELECT COUNT(*)
FROM t2

-- course solution
WITH t1 AS (
  SELECT a.name account_name, SUM(o.standard_qty) total_std, SUM(o.total) total
  FROM accounts a
  JOIN orders o
  ON o.account_id = a.id
  GROUP BY 1
  ORDER BY 2 DESC
  LIMIT 1),
t2 AS (
  SELECT a.name
  FROM orders o
  JOIN accounts a
  ON a.id = o.account_id
  GROUP BY 1
  HAVING SUM(o.total) > (SELECT total FROM t1))
SELECT COUNT(*)
FROM t2;
```
**4. For the customer that spent the most (in total over their lifetime as a customer) total_amt_usd, how many web_events did they have for each channel?**

```SQL
-- my solution
WITH t1 AS (
  SELECT a.id, a.name account, SUM(o.total_amt_usd) total_amt
  FROM accounts a
  JOIN orders o
  ON o.account_id = a.id
  GROUP BY 1, 2
  ORDER BY 3 DESC
  LIMIT 10
)
SELECT a.name account, w.channel, COUNT(*)
FROM accounts a
JOIN web_events w
ON a.id = w.account_id
JOIN t1
ON t1.id = a.id
GROUP BY 1, 2
ORDER BY 2

-- course solution
WITH t1 AS (
   SELECT a.id, a.name, SUM(o.total_amt_usd) tot_spent
   FROM orders o
   JOIN accounts a
   ON a.id = o.account_id
   GROUP BY a.id, a.name
   ORDER BY 3 DESC
   LIMIT 1)
SELECT a.name, w.channel, COUNT(*)
FROM accounts a
JOIN web_events w
ON a.id = w.account_id AND a.id =  (SELECT id FROM t1)
GROUP BY 1, 2
ORDER BY 3 DESC;
```

**5. What is the lifetime average amount spent in terms of total_amt_usd for the top 10 total spending accounts?**
```SQL
WITH t1 AS (
  SELECT a.id, a.name account, SUM(o.total_amt_usd) total_amt
  FROM accounts a
  JOIN orders o
  ON o.account_id = a.id
  GROUP BY 1, 2
  ORDER BY 3 DESC
  LIMIT 10
)

SELECT AVG(total_amt)
FROM t1
```

**6. What is the lifetime average amount spent in terms of total_amt_usd for only the companies that spent more than the average of all accounts.**
```SQL
-- my solution (incorrect)
WITH t1 AS (
  SELECT a.name, SUM(o.total_amt_usd) total_amt
  FROM accounts a
  JOIN orders o
  ON a.id = o.account_id
  GROUP BY 1
  ORDER BY 2 DESC
)
SELECT name, AVG(total_amt) avg_amt
FROM t1
GROUP BY name
HAVING AVG(total_amt) > (SELECT AVG(total_amt) FROM t1)

-- course solution
WITH t1 AS (
   SELECT AVG(o.total_amt_usd) avg_all
   FROM orders o
   JOIN accounts a
   ON a.id = o.account_id),
t2 AS (
   SELECT o.account_id, AVG(o.total_amt_usd) avg_amt
   FROM orders o
   GROUP BY 1
   HAVING AVG(o.total_amt_usd) > (SELECT * FROM t1))
SELECT AVG(avg_amt)
FROM t2;
```
