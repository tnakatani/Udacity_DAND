# Logistic Regression

## How it works
1. Predicts a probability between 0 and 1.
2. Explanatory variables can be either categorical or quantitative.
3. Coefficient outputs need to be exponentiated.
    - In order to compare the lower prestigious values to the most prestigious (the baseline), we took one over the exponential of the coefficients.
    - However, for a 1 unit increase, we could use the exponential directly.

### Example:
1. Add dummy variables
```python
df[['prest_1', 'prest_2', 'prest_3','prest_4',]] = pd.get_dummies(df['prestige'])
df.head()
```

2. Fit logistic regression model, using `prestige` with `prest_1` as baseline

  ```python
  df['intercept'] = 1

  log_mod = sm.Logit(df['admit'], df[['intercept', 'gre', 'gpa', 'prest_2', 'prest_3', 'prest_4']])
  results = log_mod.fit()
  results.summary()
  ```

3. In order to compare the lower prestigious values to the most prestigious (the baseline), we took one over the exponential of the coefficients.

  ```python
  # Exponentiate the results
  np.exp(results.params)

  # Divide by 1
  1/_
  ```

This returns:

| Variable     | Coefficient     |
| :------------- | :------------- |
| intercept   | 48.272116 |
| gre         |  0.997784 |
| gpa         |  0.458710 |
| prest_2     |  1.974147 |
| prest_3     |  3.813995 |
| prest_4     |  4.727566 |

This means for example:
- If an individual attended the most prestigious alma mater, they are 4.73 more likely to be admitted than if they attended the least prestigious, holding all other variables constant.
- For every one point increase in gpa, an individual is 2.18 more likely to be admitted, holding all other variables constant.
