def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    cities = ['chicago','new york city','washington']
    months = ['january','february','march','april','june','july']
    weekdays = ['all','monday','tuesday','wednesday','thurdsay','friday','saturday','sunday']

    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington? \n").lower()

        if city in cities:
            print("\nOK great, you have chosen " + city.title() + ". Let's move on.")
            break
        else:
            print("\nSorry, we don't have that city in our records")
            continue

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nPlease enter a month between January and June, or enter 'all' to view data from all of the months: \n").lower()

        if month in months:
            print("\nOK great, you have chosen " + month.title() + ". Let's move on.")
            break
        else:
            print("\nSorry, please choose from the name of the months, or all for every month.")
            continue

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nPlease enter a weekday, or enter 'all' to view data from all of the weekdays \n").lower()

        if day in weekdays:
            print("\nOK great, you have chosen " + day.title() + ". Let's move on.")
            break
        else:
            print("\nSorry, please choose from the name of a weekday, or all for every weekday.")
            continue

    print('-'*40)

    return city, month, day

get_filters()
