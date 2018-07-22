# Pandas

## About Pandas
- Allows the use of labels for rows and columns
- Can calculate rolling statistics on time series data
- Easy handling of NaN values
- Is able to load data of different formats into DataFrames
- Can join and merge different datasets together
- It integrates with NumPy and Matplotlib

##  Panda Series
- One-dimensional array-like object that can hold many data types, such as numbers or strings. 
- Unique point: can name the indices of your Pandas Series anything you want. 
- Can hold data of different data types, unlike ndArray in NumPy

```python
# We import Pandas as pd into Python
import pandas as pd

# We create a Pandas Series that stores a grocery list
groceries = pd.Series(data = [30, 6, 'Yes', 'No'], index = ['eggs', 'apples', 'milk', 'bread'])

# We display the Groceries Pandas Series
# eggs           30
# apples         6
# milk           Yes
# bread          No
# dtype: object
groceries
```

Display attributes:

```python
# We print some information about Groceries
# Groceries has shape: (4,)
# Groceries has dimension: 1
# Groceries has a total of 4 elements
# The data in Groceries is: [30 6 'Yes' 'No']
# The index of Groceries is: Index(['eggs', 'apples', 'milk', 'bread'], dtype='object')
print('Groceries has shape:', groceries.shape)
print('Groceries has dimension:', groceries.ndim)
print('Groceries has a total of', groceries.size, 'elements')
print('The data in Groceries is:', groceries.values)
print('The index of Groceries is:', groceries.index)
```

Check existence of attribute:
```python
# We check whether bananas is a food item (an index) in Groceries
# = False
x = 'bananas' in groceries
```

### Accessing and Deleting Elements
- `.iloc`(*location*), used for labeled index
- `.loc` (*integer location*), used for integer index
- `.drop()` - deletes items from series, but non-destructive
  - can be destructive by adding `inplace = True`

### Arithmetic Operations
- Arithmetic operations on words is possible
	- `groceries['milk] * 2` returns 'YesYes'
	- Division on words returns an error

## Panda Dataframes

### Creating a Dataframe
- Dataframe are tables created from dictionaries
- Uses `pd.Dataframe()` function
- Index labels are rows, dictionary keys are columns
- If no indexes are given, Panda uses integers instead

```python
# We create a dictionary of Pandas Series 
# Bob is key, 'bike' is a row
items = {'Bob' : pd.Series(data = [245, 25, 55], index = ['bike', 'pants', 'watch']),
         'Alice' : pd.Series(data = [40, 110, 500, 45], index = ['book', 'glasses', 'bike', 'pants'])}

# We create a Dataframe from it
shopping_cart = pd.Dataframe(items)

# Print some info about the Dataframe
print(shopping_carts.shape)
print(shopping_carts.ndim)
print(shopping_carts.size, 'elements')
print(shopping_carts.values)
print(shopping_carts.index)
print(shopping_carts.columns)

# shopping_carts has shape: (5, 2)  
# shopping_carts has dimension: 2  
# shopping_carts has a total of: 10 elements
# 
# The data in shopping_carts is:  
# [[ 500. 245.]  
# [ 40. nan]  
# [ 110. nan]  
# [ 45. 25.]  
# [ nan 55.]]
# 
# The row index in shopping_carts is: Index(['bike', 'book', 'glasses', 'pants', 'watch'], dtype='object')
# 
# The column index in shopping_carts is: Index(['Alice', 'Bob'], dtype='object')
```

### Create subsets of data from Dataframe:
```python
# We Create a DataFrame that only has Bob's data
bob_shopping_cart = pd.DataFrame(items, columns=['Bob'])

# We Create a DataFrame that only has selected items for both Alice and Bob
sel_shopping_cart = pd.DataFrame(items, index = ['pants', 'book'])

# We Create a DataFrame that only has selected items for Alice
alice_sel_shopping_cart = pd.DataFrame(items, index = ['glasses', 'bike'], columns = ['Alice'])
```

### Create Dataframes from a dictionary of lists.  
```python
# We create a dictionary of lists (arrays)
data = {'Integers' : [1,2,3],
        'Floats' : [4.5, 8.2, 9.6]}

# We create a dataframe from it, no index results in numbered row index   
df = pd.Dataframe(data)

# We create a DataFrame and provide the row index
df2 = pd.DataFrame(data, index = ['label 1', 'label 2', 'label 3'])
```
- Note that all lists must be the same length.

### Create Dataframes using a list of Python dictionaries
```python
# We create a list of Python dictionaries
items2 = [{'bikes': 20, 'pants': 30, 'watches': 35}, 
          {'watches': 10, 'glasses': 50, 'bikes': 15, 'pants':5}]

# We create a DataFrame 
store_items = pd.DataFrame(items2)

# Can also create list with labeled index
store_items = pd.DataFrame(items2, index = ['store 1', 'store 2'])
```

### Accessing Elements
```python
# We access rows, columns and elements using labels (using store_items data above)
print('How many bikes are in each store:\n', store_items[['bikes']])
print('How many bikes and pants are in each store:\n', store_items[['bikes', 'pants']])
print('What items are in Store 1:\n', store_items.loc[['store 1']])
print('How many bikes are in Store 2:', store_items['bikes']['store 2']) # dataset[column][row] format
```

- When accessing individual elements in a DataFrame (last example), need to have column first, like `dataset[column][row]`

### Adding Elements
```python
# We add a new column named shirts to our store_items DataFrame indicating the number of
# shirts in stock at each store. We will put 15 shirts in store 1 and 2 shirts in store 2
store_items['shirts'] = [15,2]
```

-  When adding columns, it is appended to the end

### Using Arithmetic
```python
# We make a new column called suits by adding the number of shirts and pants
store_items['suits'] = store_items['pants'] + store_items['shirts']
```

### Adding Rows
```python
# We create a dictionary from a list of Python dictionaries that will number of items at the new store
new_items = [{'bikes': 20, 'pants': 30, 'watches': 35, 'glasses': 4}]

# We create new DataFrame with the new_items and provide and index labeled store 3
new_store = pd.DataFrame(new_items, index = ['store 3'])

# We append store 3 to our store_items DataFrame
store_items = store_items.append(new_store)
```

- If appending a new row with new columns, the columns will be alphabetized

### Adding Columns
- Add new columns of our DataFrame by using only data from particular rows in particular columns:

```python
# We add a new column using data from particular rows in the watches column
store_items['new watches'] = store_items['watches'][1:]
```

- Insert new columns into a Dataframe using the format `dataset.insert(index, column name, data)`:

```python
# We insert a new column with label shoes right before the column with numerical index 4
store_items.insert(4, 'shoes', [8,5,0])
```

### Deleting Row/Columns
- Delete a column using `.pop()`

```python
# We remove new watches column
store_items = store_items.pop('new watches')
```

- Delete column/row using `.drop()` + `axis` keyword.  
- `axis=1` for columns, `axis=2` for rows

```python
# We remove more than one column
store_items = store_items.drop(['shoes','pants'], axis=1)

# We remove more than one row
store_items = store_items.drop(['store 1', 'store 3'], axis=2)
```

### Changing Label Names
- `.rename()` uses dictionary format

```python
# Change column name
store_items = store_items.rename(columns = {'bikes' : 'hats'})

# Change row name
store_items = store_items.rename(rows = {'store 1' : 'store 8'})
```

### Changing Indexes

```python
# We change the row index to be the data in the pants column
store_items = store_items.set_index('pants')
```

## Dealing with `NaN`

Example dataset:

```python
# We create a list of Python dictionaries
items2 = [{'bikes': 20, 'pants': 30, 'watches': 35, 'shirts': 15, 'shoes':8, 'suits':45},
{'watches': 10, 'glasses': 50, 'bikes': 15, 'pants':5, 'shirts': 2, 'shoes':5, 'suits':7},
{'bikes': 20, 'pants': 30, 'watches': 35, 'glasses': 4, 'shoes':10}]

# We create a DataFrame  and provide the row index
store_items = pd.DataFrame(items2, index = ['store 1', 'store 2', 'store 3'])
```

### Count `NaN` values

Use `.isnull()` and `.sum()`
- `.isnull()` returns Boolean Dataframe, `True` for NaN and `False` for elements that are not.  `True` is `1` so we can `sum()` it.
- Need to use `sum()` twice bc first sum returns Pandas Series, and `sum()` again returns all the `1` in the series.

```python
# Count number of NaN values
x = store_items.isnull().sum().sum()
```

### Count non-`NaN` values

Use `.count()` method

```python
x = store_items.count()
```

### Delete `NaN` values

- The `.dropna(axis)` method eliminates any rows with `NaN` values when `axis = 0` is used and will eliminate any columns with NaN values when `axis = 1` is used. 
- `.dropna(axis)` is not destructive. Can be destructive with `inplace = True` inside `dropna()`

```python
# Drop any rows with NaN values
store_items.dropna(axis=0)

# Drop any columns with NaN values
store_items.dropna(axis=1)
```

### Replace `NaN` values

```python
# Replace all NaN values with 0
store_items.fillna(0)

# Replace NaN with previous value in the column
store_items.fillna(method = 'ffill', axis=0)

# Replace NaN with previous value in the row
store_items.fillna(method = 'ffill', axis=1)

# Replace NaN with next value in the column
store_items.fillna(method = 'backfill', axis=0)

# Replace NaN with next value in the row
store_items.fillna(method = 'backfill', axis=1)

# Replace NaN with linear interpolation using column values
store_items.interpolate(method = 'linear', axis = 0)

# Replace NaN with linear interpolation using row values
store_items.interpolate(method = 'linear', axis = 1)
```

### Challenge: Manipulate a Dataframe
```pyton
import pandas as pd
import numpy as np

# Since we will be working with ratings, we will set the precision of our 
# dataframes to one decimal place.
pd.set_option('precision', 1)

# Create a Pandas DataFrame that contains the ratings some users have given to a
# series of books. The ratings given are in the range from 1 to 5, with 5 being
# the best score. The names of the books, the authors, and the ratings of each user
# are given below:

books = pd.Series(data = ['Great Expectations', 'Of Mice and Men', 'Romeo and Juliet', 'The Time Machine', 'Alice in Wonderland' ])
authors = pd.Series(data = ['Charles Dickens', 'John Steinbeck', 'William Shakespeare', ' H. G. Wells', 'Lewis Carroll' ])

user_1 = pd.Series(data = [3.2, np.nan ,2.5])
user_2 = pd.Series(data = [5., 1.3, 4.0, 3.8])
user_3 = pd.Series(data = [2.0, 2.3, np.nan, 4])
user_4 = pd.Series(data = [4, 3.5, 4, 5, 4.2])

# Users that have np.nan values means that the user has not yet rated that book.
# Use the data above to create a Pandas DataFrame that has the following column
# labels: 'Author', 'Book Title', 'User 1', 'User 2', 'User 3', 'User 4'. Let Pandas
# automatically assign numerical row indices to the DataFrame. 

# Create a dictionary with the data given above
dat = {
    'Author' : authors,
    'Book Title' : books,
    'User 1' : user_1,
    'User 2' : user_2,
    'User 3' : user_3,
    'User 4' : user_4
}

# Use the dictionary to create a Pandas DataFrame
book_ratings = pd.DataFrame(dat)

# If you created the dictionary correctly you should have a Pandas DataFrame
# that has column labels: 'Author', 'Book Title', 'User 1', 'User 2', 'User 3',
# 'User 4' and row indices 0 through 4.

# Now replace all the NaN values in your DataFrame with the average rating in
# each column. Replace the NaN values in place. HINT: you can use the fillna()
# function with the keyword inplace = True, to do this. Write your code below:
book_ratings = book_ratings.fillna(book_ratings.mean(), axis=0, inplace = True)
```

## Loading Data into a Pandas Dataframe

### Read CSV file

```python
Google_stock = pd.read_csv('./GOOG.csv')
```

### Useful methods
- `.head()` - show first 5 rows of data
- `.tail()` - show last 5 rows
  - can use `.head(N)` or `.tail(N)` for `N` rows of data
- `.isnull().any()` - check if any columns contain `NaN`
- `.describe()` - show statistical data (count, mean, std, min, etc)
  - can use method on single column via `dataframe['column'].describe()`
  - can use specific methods (`.max()`, `.min()`, `.mean()`)
- `.corr` -  show correlation (1 = high correlation)
- `.groupby()` - show grouped data via `dataframe.groupby(['column'])`

```python
# Display total amount of money spent in salaries each year
data.groupby(['Year'])['Salary'].sum()

# Theoretically returns:
# Year
# 1990     153000
# 1991     162000
# 1992     174000

# Display avg salary per year
data.groupby(['Year'])['Salary'].mean()

# Display total salary each employee received in all the years worked
data.groupby(['Name'])['Salary'].sum()

# Display salary distro per department per year
data.groupby(['Year', 'Department'])['Salary'].sum()

Year    Department
1990    Admin         55000
        HR            50000
        RD            48000
1991    Admin         60000
        HR            52000
        RD            50000
1992    Admin         122000
        RD            52000

```









