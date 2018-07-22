import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Global variables
cities = ['chicago','new york city','washington']
months = ['january','february','march','april','may','june','july','all']
weekdays = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']

# Helper function for humanizing time data
def convert_to_d_h_m_s(seconds):
    """
    Return dictionary of days, hours, minutes and seconds.
    """

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    return {'days':days, 'hours':hours, 'minutes':minutes, 'seconds':seconds}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print("Hello! Let's explore some US bikeshare data! \n")

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington? \n").lower()

        if city in cities:
            print("\nOK great, you have chosen " + city.title() + ". Let's move on.")
            break
        else:
            print("\nSorry, we don't have that city in our records. \n")
            continue

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nPlease enter a month between January and June, or enter 'all' to view data from all of the months: \n").lower()

        if month in months:
            print("\nOK great, you have chosen " + month.title() + ". Let's move on.")
            break
        else:
            print("\nSorry, please choose a month between January and June, or all for every month.")
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


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month)+1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df =  df[df['day_of_week'] == day.title()]

    return df

def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('Calculating The Most Frequent Times of Travel in ' + city.title() + '...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        print('Calculating the most popular month...')

        common_month = df['month'].mode()[0]
        print('The most popular month is: ' + months[common_month - 1].title() + '\n')

    # display the most common day of week
    if day == 'all':
        print('Calculating the most popular weekday...')

        common_day = df['day_of_week'].mode()[0]
        print('The most popular weekday is: ' + common_day + '\n')

    # display the most common start hour
    print('Calculating the most popular start hour...')

    common_hour= df['Start Time'].dt.strftime("%I:00%p").mode()[0] #.dt.strftime("%I:00%p")
    print('The most popular start hour is: ' + str(common_hour) + '\n')

    print("This took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df, city, month):
    """Displays statistics on the most popular stations and trip."""

    start_time = time.time()

    # display the most common month
    if month == 'all':
       print('\nCalculating The Most Popular Stations and Trip in ' + city.title() + '...\n')
    else:
       print('\nCalculating The Most Popular Stations and Trip in ' + city.title() + ' During ' + month.title() + '...\n')

    # display most commonly used start station
    common_start_station = df['Start Station'].value_counts().index[0]
    print('The most popular start station is: ' + common_start_station + '\n')

    # display most commonly used end station
    common_end_station = df['End Station'].value_counts().index[0]
    print('The most popular end station is: ' + common_end_station + '\n')

    # display most frequent combination of start station and end station trip
    trips = df.groupby(['Start Station','End Station']).count().sort_values('Unnamed: 0',ascending=False).index[0]
    common_trip_start, common_trip_end = trips

    print('The most frequent combination of start / end station is:')
    print('Start Station: ' + common_trip_start + '\nEnd Station: ' + common_trip_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df, city, month):
    """Displays statistics on the total and average trip duration."""

    start_time = time.time()

    if month == 'all':
       print('\nCalculating Trip Duration in ' + city.title() + '...\n')
    else:
       print('\nCalculating Trip Duration in ' + city.title() + ' During ' + month.title() + '...\n')

    # display total travel time
    total_travel_time = convert_to_d_h_m_s(df['Trip Duration'].sum())
    tt_days = int(total_travel_time['days'])
    tt_hours = int(total_travel_time['hours'])
    tt_minutes = int(total_travel_time['minutes'])
    tt_seconds = int(total_travel_time['seconds'])
    print('Total travel duration of all riders was: '
           + str(tt_days) + ' days, '
           + str(tt_hours) + ' hours, '
           + str(tt_minutes) + ' minutes, and '
           + str(tt_seconds) + ' seconds.'
    )

    # display mean travel time
    mean_travel_time = convert_to_d_h_m_s(df['Trip Duration'].mean())
    m_hours = int(mean_travel_time['hours'])
    m_minutes = int(mean_travel_time['minutes'])
    m_seconds = int(mean_travel_time['seconds'])
    print('\nAverage travel duration of all riders was: '
           + str(m_minutes) + ' minutes and '
           + str(m_seconds) + ' seconds.'
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city, month):
    """Displays statistics on bikeshare users."""

    start_time = time.time()

    if month == 'all':
       print('\nCalculating Statistics on Bikeshare Users in ' + city.title() + '...\n')
    else:
       print('\nCalculating Statistics on Bikeshare Users in ' + city.title() + ' During ' + month.title() + '...\n')

    # Display counts of user types
    if 'User Type' in df.columns:
        user_types = df.groupby(['User Type']).size().reset_index(name='count')

        print('The breakdown of user types are listed below:')
        for index, row in user_types.iterrows():
            print(row["User Type"] + ': ' + str(row["count"]))

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_types = df.groupby(['Gender']).size().reset_index(name='count')

        print('\nThe breakdown of gender is listed below:')
        for index, row in gender_types.iterrows():
            print(row["Gender"] + ': ' + str(row["count"]))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        year_of_birth = df.sort_values(by=['Birth Year'])
        yob_earliest = int(year_of_birth['Birth Year'].min())
        yob_recent = int(year_of_birth['Birth Year'].max())
        yob_common = int(year_of_birth['Birth Year'].mean())

        print('\nThe breakdown of birth years are listed below:')
        print('Earliest birth year was: ' + str(yob_earliest))
        print('Most recent birth year was: ' + str(yob_recent))
        print('Average birth year was: ' + str(yob_common))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, city, month, day)
        station_stats(df, city, month)
        trip_duration_stats(df, city, month)
        user_stats(df, city, month)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
