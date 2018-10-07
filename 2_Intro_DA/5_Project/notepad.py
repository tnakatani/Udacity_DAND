years = list(range(1998,2019))

for year in years:
  'df1_' + str(year) = df1_by_year.loc[str(year)]


da````````

# Calculate mean of each column (for filling in null cells)
permit = df1['permit'].mean()
handgun = df1['handgun'].mean()
long_gun = df1['long_gun'].mean()
other = df1['other'].mean()

# Replace null cells with the mean of each column
df1['permit'].fillna(permit, inplace=True)
df1['handgun'].fillna(handgun, inplace=True)
df1['long_gun'].fillna(long_gun, inplace=True)
df1['other'].fillna(other, inplace=True)
