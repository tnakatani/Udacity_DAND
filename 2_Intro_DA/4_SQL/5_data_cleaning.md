# Data Cleaning

## `LEFT` / `RIGHT` / `LENGTH`
`LEFT` pulls a specified number of characters for each row in a specified column starting at the beginning (or from the left).


`RIGHT` pulls a specified number of characters for each row in a specified column starting at the end (or from the right).

`LENGTH` provides the number of characters for each row of a specified column.

Example: Using `phone_number` column with data like "724-657-1550":
```SQL
-- Get area code with LEFT
LEFT(phone_number, 3) -- returns 724

-- Get phone number with RIGHT
RIGHT(phone_number, 8) -- returns 657-1550

-- Get character count with LENGTH
LENGTH(phone_number) -- returns 12

-- Get phone number using RIGHT + LENGTH
RIGHT(phone_number, LENGTH(phone_numer) - 4) -- return 657-1550
```

### Quiz Pt.1
1. In the accounts table, there is a column holding the website for each company. The last three digits specify what type of web address they are using. Pull these extensions and provide how many of each website type exist in the accounts table.
  ```SQL
  SELECT RIGHT(website, 4),
         COUNT(RIGHT(website, 4))
  FROM accounts
  GROUP BY 1
  ORDER BY count DESC
  ```

2. There is much debate about how much the name (or even the first letter of a company name) matters. Use the accounts table to pull the first letter of each company name to see the distribution of company names that begin with each letter (or number).
  ```SQL
  WITH t1 AS (
    SELECT LEFT(RIGHT(website, LENGTH(website) - 4), 1) AS first_letter,
    a.name
    FROM accounts a
  )

  SELECT t1.first_letter,
  	     COUNT(*)
  FROM t1
  GROUP BY 1
  ORDER BY count DESC
  ```

3. Use the accounts table and a `CASE` statement to create two groups: one group of company names that start with a number and a second group of those company names that start with a letter. What proportion of company names start with a letter?  
  ```SQL
  WITH t1 AS (
  SELECT name,
        -- create 2 binary columns  
         CASE WHEN LEFT((name), 1) IN ('0','1','2','3','4','5','6','7','8','9') THEN 1 ELSE 0 END AS number,
         CASE WHEN LEFT((name), 1) IN ('0','1','2','3','4','5','6','7','8','9') THEN 0 ELSE 1 END AS letter
    FROM accounts
    ORDER BY name
  )

  SELECT SUM(number) AS num_count, SUM(letter) AS letter_count
  FROM t1
  ```

4. Consider vowels as a, e, i, o, and u. What proportion of company names start with a vowel, and what percent start with anything else?
```SQL
WITH t1 AS (
  SELECT name,
         CASE WHEN LEFT((LOWER(name)), 1) IN ('a','e','i','o','u') THEN 1 ELSE 0 END AS letter
  FROM accounts
)
SELECT SUM(letter),
       COUNT(*)
FROM t1
```

## `POSITION`, `STRPOS`, & `SUBSTR`
1. `POSITION` - takes a character and a column, and provides the index where that character is for each row. Here, you saw that you can pull the index of a comma as `POSITION(',' IN city_state)`.
  - Note that index in SQL is 1, not 0.
2. `STRPOS` - provides the same result as `POSITION`, but the syntax for achieving those results is a bit different as shown here: `STRPOS(city_state, ',')`.
  - Note that both functions are case sensitive.
3. `LOWER` / `UPPER` - makes strings lowercase / uppercase.

## Quiz Pt. 2
1. Use the accounts table to create first and last name columns that hold the first and last names for the `primary_poc`.
  ```SQL
  SELECT primary_poc,
         LEFT(primary_poc, POSITION(' ' IN primary_poc)) AS first,
         RIGHT(primary_poc, LENGTH(primary_poc) - POSITION(' ' IN primary_poc)) AS last
  FROM accounts
  ```

2. Now see if you can do the same thing for every rep name in the `sales_reps` table. Again provide first and last name columns.
  ```SQL
  SELECT name,
         LEFT(name, POSITION(' ' IN name)) AS first,
         RIGHT(name, LENGTH(name) - POSITION(' ' IN name)) AS last
  FROM sales_reps
  ```

## `CONCAT` and  `||`

Each of these will allow you to combine columns together across rows.

```SQL
-- using CONCAT
CONCAT(first_name, ' ', last_name)
-- or with piping
first_name || ' ' || last_name.
```

### Quiz Pt. 3
1 & 2. Each company in the accounts table wants to create an email address for each primary_poc. The email address should be the first name of the `primary_poc` . last name `primary_poc` @ company name .com.

  ```SQL
  WITH t1 AS (
    SELECT
    LOWER(LEFT(primary_poc, POSITION(' ' IN primary_poc) - 1)) AS first,
    LOWER(RIGHT(primary_poc, LENGTH(primary_poc) - POSITION(' ' IN primary_poc))) AS last,
    REPLACE(LOWER(name), ' ', '') AS concat_name
    FROM accounts
  )

  SELECT CONCAT(t1.first, t1.last,'@',concat_name,'.com')
  FROM t1                                    
  ```
3. We would also like to create an initial password, which they will change after their first log in. The first password will be the first letter of the primary_poc's first name (lowercase), then the last letter of their first name (lowercase), the first letter of their last name (lowercase), the last letter of their last name (lowercase), the number of letters in their first name, the number of letters in their last name, and then the name of the company they are working with, all capitalized with no spaces.

```SQL
-- Table of first & last name
WITH t1 AS (
  SELECT id,
         REPLACE(UPPER(name), ' ', '') AS concat_name,
         LEFT(LOWER(primary_poc), POSITION(' ' IN primary_poc) - 1) AS first,
         RIGHT(LOWER(primary_poc), LENGTH(primary_poc) - POSITION(' ' IN primary_poc)) AS last
  FROM accounts
),
-- Table of password components
t2 AS (
  SELECT id,
         LEFT(first, 1) AS first_1,
         RIGHT(first, 1) AS first_2,
         LEFT(last, 1) AS last_1,
         RIGHT(last,1) AS last_2,
         LENGTH(first) AS first_length,
         LENGTH(last) AS last_length,
         concat_name
  FROM t1
),
t3 AS (
  SELECT id,
         CONCAT(first, last,'@',LOWER(concat_name),'.com') AS email
  FROM t1
)

SELECT t3.email,
       CONCAT(first_1,first_2,last_1,last_2,first_length,last_length,t2.concat_name) AS password
FROM t2
JOIN t3
ON t2.id = t3.id
```

## `CAST` / `::`
`CAST` is useful for changing column types. Commonly you might be changing a string to a date using `CAST(date_column AS DATE)`.

You can also use `date_column::DATE` as a shorthand (like `||` for `CONCAT`).

#### Note on `CAST` and implicit casting
- Most of the functions presented in this lesson are specific to strings. They won’t work with dates, integers or floating-point numbers.
- However, using any of these functions will automatically change the data to the appropriate type.
- `LEFT`, `RIGHT`, and `TRIM` are all used to select only certain elements of strings, but using them to select elements of a number or date will treat them as strings for the purpose of the function.

### Quiz Pt. 4
Write a query changing unformatted date data to correct SQL date format using `CAST`.
```SQL
WITH t1 AS (
  SELECT date,
       SUBSTR(date,1,2) AS month,
       SUBSTR(date,4,2) AS day,
       SUBSTR(date,7,4) AS year
  FROM sf_crime_data
)
SELECT CONCAT(year,'-',month,'-',day)::DATE
FROM t1
```

## `COALESCE`
`COALESCE` returns the first non-NULL value passed for each row.

```SQL
SELECT COALESCE(primary_poc, 'no POC')
FROM accounts
```

#### Quit Pt. 5
1.
```SQL
SELECT *,
       COALESCE(a.id, a.id) AS id,
       COALESCE(o.account_id, a.id) AS account_id,
       COALESCE(standard_qty, 0) AS standard_qty,
       COALESCE(gloss_qty, 0) AS gloss_qty,
       COALESCE(poster_qty, 0) AS poster_qty,
       COALESCE(total, 0) AS total,
       COALESCE(standard_amt_usd, 0) AS standard_amt_usd,
       COALESCE(gloss_amt_usd, 0) AS gloss_amt_usd,
       COALESCE(poster_amt_usd, 0) AS poster_amt_usd,
       COALESCE(total_amt_usd, 0) AS total_amt_usd
FROM accounts a
LEFT JOIN orders o
ON a.id = o.account_id
WHERE o.total IS NULL;
```
