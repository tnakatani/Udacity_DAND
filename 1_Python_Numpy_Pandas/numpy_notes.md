# numpy notes


## Formulas

```python
# Create a 4 x 4 diagonal matrix that contains the numbers 10,20,30, and 50
# on its main diagonal
X = np.diag([10,20,30,50])

# We create a rank 1 ndarray that has sequential integers from 0 to 9
x = np.arange(10)

# We create a rank 1 ndarray that has sequential integers from 4 to 9. 
x = np.arange(4,10)

# We create a rank 1 ndarray that has evenly spaced integers from 1 to 13 in steps of 3.
x = np.arange(1,14,3)

# We create a rank 1 ndarray that has 10 integers evenly spaced between 0 and 25.
x = np.linspace(0,25,10)

‭# We create a rank 1 ndarray that has 10 integers evenly spaced between 0 and 25,‬
‭# with 25 excluded.‬
‭x = np.linspace(0,25,10, endpoint = False)‬

# We create a rank 1 ndarray with 10 integers evenly spaced between 0 and 50,
# with 50 excluded. We then reshape it to a 5 x 2 ndarray
X = np.linspace(0,50,10, endpoint=False).reshape(5,2)

# random floats in the half-open interval [0.0, 1.0)
np.random.random(shape)

# We create a 1000 x 1000 ndarray of random floats drawn from normal (Gaussian) distribution
# with a mean of zero and a standard deviation of 0.1.
X = np.random.normal(0, 0.1, size=(1000,1000))
```


## Accessing / Deleting / Modifying

```python
# We create a 3 x 3 rank 2 ndarray that contains integers from 1 to 9
X = np.array([[1,2,3],[4,5,6],[7,8,9]])

# Let's access some elements in X
# [0, 0] refers to the element in the first row, first column.
print('This is (0,0) Element in X:', X[0,0]) # 1
print('This is (0,1) Element in X:', X[0,1]) # 2
print('This is (2,2) Element in X:', X[2,2]) # 9
```


### Deleting

```python
# We create a rank 1 ndarray 
x = np.array([1, 2, 3, 4, 5])

# We delete the first and last element of x
x = np.delete(x, [0,4])

# We create a rank 2 ndarray
Y = np.array([[1,2,3],[4,5,6],[7,8,9]])

# We delete the first row of y ([1,2,3] gets deleted)
w = np.delete(Y, 0, axis=0)

# We delete the first and last column of y
# = [[2][5][8]])
v = np.delete(Y, [0,2], axis=1)
```


### Appending

```python
# We create a rank 1 ndarray 
x = np.array([1, 2, 3, 4, 5])

# We append the integer 7 and 8 to x
# =([1,2,3,4,5,6,7,8])
x = np.append(x, [7,8])

# We create a rank 2 ndarray 
Y = np.array([[1,2,3],[4,5,6]])

# We append a new row containing 7,8,9 to y
# = [[1 2 3] [4 5 6] [7 8 9]]
v = np.append(Y, [[7,8,9]], axis=0)

# We append a new column containing 9 and 10 to y
# = [[1 2 3 9] [4 5 6 10]]
q = np.append(Y,[[9],[10]], axis=1)
```


## Inserting Arrays

```python
# We create a rank 1 ndarray 
x = np.array([1, 2, 5, 6, 7])

# We insert the integer 3 and 4 between 2 and 5 in x. 
# np.insert(ndarray, index, elements, axis)
# = [1 2 5 6 7]
x = np.insert(x,2,[3,4])

# We create a rank 2 ndarray 
Y = np.array([[1,2,3],[7,8,9]])

# We insert a row between the first and last row of y
# =[[1 2 3] [4 5 6] [7 8 9]]
w = np.insert(Y,1,[4,5,6],axis=0)

# We insert a column full of 5s between the first and second column of y
# = [[1 5 2 3] [7 5 8 9]]
v = np.insert(Y,1,5, axis=1)
```


## Stacking Arrays

```python
# We create a rank 1 ndarray 
x = np.array([1,2])

# We create a rank 2 ndarray 
Y = np.array([[3,4],[5,6]])

# We stack x on top of Y
# = [[1 2] [3 4] [5 6]]
z = np.vstack((x,Y))

# We stack x on the right of Y. We need to reshape x in order to stack it on the right of Y. 
# = [[3 4 1] [5 6 2]]
w = np.hstack((Y,x.reshape(2,1)))
```


## Slicing Arrays

Main Types:
1. `ndarray[start:end]`
2. `ndarray[start:]`
3. `ndarray[:end]`

```python
# We create a 4 x 5 ndarray that contains integers from 0 to 19
# = [[ 0 1 2 3 4] [ 5 6 7 8 9] [10 11 12 13 14] [15 16 17 18 19]]
X = np.arange(20).reshape(4, 5)

# We select all the elements that are in the 2nd through 4th rows and in the 3rd to 5th columns
# = [[ 7 8 9] [12 13 14] [17 18 19]]
Z = X[1:4,2:5]

# We can select the same elements as above using method 2
# = [[ 7 8 9] [12 13 14] [17 18 19]]
W = X[1:,2:5]

# We select all the elements that are in the 1st through 3rd rows and in the 3rd to 4th columns
# = [[ 2 3 4] [ 7 8 9] [12 13 14]]
Y = X[:3,2:5]

# We select all the elements in the 3rd row
# = [10 11 12 13 14]
v = X[2,:]

# We select all the elements in the 3rd column
# = [ 2 7 12 17]
q = X[:,2]

# We select all the elements in the 3rd column but return a rank 2 ndarray
# =[[ 2] [ 7] [12] [17]]
R = X[:,2:3]
```

## Copying Arrays

It is important to note that when we perform slices on ndarrays and save them into new variables, as we did above, the data is not copied into the new variable.

If we want to create a new ndarray that contains a copy of the values in the slice we need to use the np.copy().  It can be used either as a function `np.copy(ndarray)` or a method `.copy()`.

```python
# create a copy of the slice using the np.copy() function
Z = np.copy(X[1:4,2:5])
```

## Indices

```python
# We create a 4 x 5 ndarray that contains integers from 0 to 19
# [[ 0 1 2 3 4] [ 5 6 7 8 9] [10 11 12 13 14] [15 16 17 18 19]]
X = np.arange(20).reshape(4, 5)

# We create a rank 1 ndarray that will serve as indices to select elements from X
indices = np.array([1,3])

# We use the indices ndarray to select the 2nd and 4th row of X
# = [[ 5 6 7 8 9] [15 16 17 18 19]]
Y = X[indices,:]

# We use the indices ndarray to select the 2nd and 4th column of X
# = [[ 1 3] [ 6 8] [11 13] [16 18]]
Z = X[:, indices]
```


## Built-in Functions

```python
# Create 3 x 3 ndarray with repeated values
# [[1 2 3] [5 2 8] [1 2 3]]
X = np.array([[1,2,3],[5,2,8],[1,2,3]])

# We print the unique elements of X 
print('The unique elements in X are:',np.unique(X))
```

## Boolean Indexing

Boolean indexing can help us select elements using logical arguments instead of explicit indices.

```python
# We create a 5 x 5 ndarray that contains integers from 0 to 24
# = [[ 0 1 2 3 4] [ 5 6 7 8 9] [10 11 12 13 14] [15 16 17 18 19] [20 21 22 23 24]]
X = np.arange(25).reshape(5, 5)

# [11 12 13 14 15 16 17 18 19 20 21 22 23 24]'
print(X[X > 10])

# [0 1 2 3 4 5 6 7]
print(X[X <= 7])

# [11 12 13 14 15 16]
print(X[(X > 10) & (X < 17)])

# We use Boolean indexing to assign the elements that are between 10 and 17 the value of -1
# = [[ 0 1 2 3 4] [ 5 6 7 8 9] [10 -1 -1 -1 -1] [-1 -1 17 18 19] [20 21 22 23 24]]
X[(X > 10) & (X < 17)] = -1
```

Set operations allows comparison of ndarrays for common elements.

```python
# We create a rank 1 ndarray
x = np.array([1,2,3,4,5])

# We create a rank 1 ndarray
y = np.array([6,7,2,8,4])

# = [2 4]
print('The elements that are both in x and y:', np.intersect1d(x,y))

# = [1 3 5]
print('The elements that are in x that are not in y:', np.setdiff1d(x,y))

# = [1 2 3 4 5 6 7 8]
print('All the elements of x and y:',np.union1d(x,y))
```


## Sorting

The `sort` function can be used either as a function `np.sort()` or a method `ndarray.sort()`

Beware that:
- When `np.sort()` is used as a function, it does not change original array.
- When used as a method, it changes the original array.

```python
# We create an unsorted rank 1 ndarray
# = [9 6 4 4 9 4 8 4 4 7]
x = np.random.randint(1,11,size=(10,))

# We sort x and print the sorted array using sort as a function.
# = [4 4 4 4 4 6 7 8 9 9]
print(np.sort(x))

# When we sort out of place the original array remains intact.
# = [9 6 4 4 9 4 8 4 4 7]
print(x)
```

When sorting rank 2 ndarrays, we need to specify to the np.sort() function whether we are sorting by rows or columns. This is done by using the axis keyword.

```python
# We create an unsorted rank 2 ndarray
# [[6 1 7 6 3]
#  [3 9 8 3 5]
#  [6 5 8 9 3]
#  [2 1 5 7 7]
#  [9 8 1 9 8]]
X = np.random.randint(1,11,size=(5,5))

# We sort the columns of X and print the sorted array
# [[2 1 1 3 3]
#  [3 1 5 6 3]
#  [6 5 7 7 5]
#  [6 8 8 9 7]
#  [9 9 8 9 8]]
print(np.sort(X, axis = 0))

# We sort the rows of X and print the sorted array
# [[1 3 6 6 7]
#  [3 3 5 8 9]
#  [3 5 6 8 9]
#  [1 2 5 7 7]
#  [1 8 8 9 9]]
print(np.sort(X, axis = 1))
```


## Arithmetic Operations & Broadcasting

numPy can:
- Use built-in functions like `np.add()` or,
- Use arithmetic operators like `+`

```python
# We create two rank 1 ndarrays
x = np.array([1,2,3,4])
y = np.array([5.5,6.5,7.5,8.5])

# = [ 6.5 8.5 10.5 12.5]
print(x + y)
print(add(x,y))

# = [-4.5 -4.5 -4.5 -4.5]
print(x - y)
print(subtract(x,y))

# = [ 5.5 13. 22.5 34. ]
print(x * y)
print(multiply(x,y))

# = [ 0.18181818 0.30769231 0.4 0.47058824]
print(x / y)
print(divide(x,y))
```

Can also be performed on rank 2 arrays:

```python
# We create two rank 2 ndarrays

# [[1 2] [3 4]]
X = np.array([1,2,3,4]).reshape(2,2)
# [[ 5.5 6.5] [ 7.5 8.5]]
Y = np.array([5.5,6.5,7.5,8.5]).reshape(2,2)

# = [[ 6.5 8.5] [ 10.5 12.5]]
print(X + Y)
print(add(X,Y))

# et al.

```

Can also use mathematical functions:

```python
# We create a rank 1 ndarray
x = np.array([1,2,3,4])

# We apply different mathematical functions to all elements of x
# = [ 2.71828183 7.3890561 20.08553692 54.59815003]
print(np.exp(x))

# = [ 1. 1.41421356 1.73205081 2. ]
print(np.sqrt(x))

# = [ 1 4 9 16]
print(np.power(x,2)) # We raise all elements to the power of 2

```

Can also use statistical functions:

```python
# We create a 2 x 2 ndarray
X = np.array([[1,2], [3,4]])

print('Average of all elements in X:', X.mean())
print('Average of all elements in the columns of X:', X.mean(axis=0))
print('Average of all elements in the rows of X:', X.mean(axis=1))

print('Sum of all elements in X:', X.sum())
print('Sum of all elements in the columns of X:', X.sum(axis=0))
print('Sum of all elements in the rows of X:', X.sum(axis=1))

print('Standard Deviation of all elements in X:', X.std())
print('Standard Deviation of all elements in the columns of X:', X.std(axis=0))
print('Standard Deviation of all elements in the rows of X:', X.std(axis=1))

print('Median of all elements in X:', np.median(X))
print('Median of all elements in the columns of X:', np.median(X,axis=0))
print('Median of all elements in the rows of X:', np.median(X,axis=1))

print('Maximum value of all elements in X:', X.max())
print('Maximum value of all elements in the columns of X:', X.max(axis=0))
print('Maximum value of all elements in the rows of X:', X.max(axis=1))

print('Minimum value of all elements in X:', X.min())
print('Minimum value of all elements in the columns of X:', X.min(axis=0))
print('Minimum value of all elements in the rows of X:', X.min(axis=1))

```

NumPy can add single numbers to all the elements of an ndarray without the use of complicated loops.  It uses something called *broadcasting* to do this.

```python
# We create a 2 x 2 ndarray
X = np.array([[1,2], [3,4]])

# = [[ 3 6] [ 9 12]]
print(3 * X)

# = [[4 5] [6 7]]
print(3 + X)

# = [[-2 -1] [ 0 1]]
print(X - 3)

# = [[ 0.33333333 0.66666667] [ 1. 1.33333333]]
print(X / 3)
```

Numpy can do the same for two ndarrays of different shapes.

```python
# We create a rank 1 ndarray
x = np.array([1,2,3])

# We create a 3 x 3 ndarray
# [[1 2 3]
#  [4 5 6]
#  [7 8 9]]
Y = np.array([[1,2,3],[4,5,6],[7,8,9]])

# We create a 3 x 1 ndarray
# [[1]
#  [2]
#  [3]]
Z = np.array([1,2,3]).reshape(3,1)

# [[ 2 4 6]
#  [ 5 7 9]
#  [ 8 10 12]]
print(x + Y) # add x to each row

# [[ 2 3 4]
#  [ 6 7 8]
#  [10 11 12]]
print(Z + Y) # add Y to each row sequentially
```

	