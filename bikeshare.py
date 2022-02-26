import time
import datetime as dt
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('\nWould you like to see data for ' + '{0}, {1},'.format(*CITY_DATA).title() + ' or ' + '{2}?\n'.format(*CITY_DATA).title()).lower().strip()
    while city not in [*CITY_DATA]:
        city = input('\nCity entered was not recognized. Please enter one of the following cities: ' + '{0}, {1},'.format(*CITY_DATA).title() + ' or ' + '{2}.\n'.format(*CITY_DATA).title()).lower().strip()

    # get user input for month (all, january, february, ... , june)
    month = input('\nPlease enter a month from January-June or enter All.\n').lower().strip()
    while month not in months and month != 'all':
        month = input('\nThat was not a valid selection. Please enter a month from the following: January, February, March, April, May, June or All.\n').lower().strip()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('\nPlease enter a day from Monday-Sunday or enter All.\n').lower().strip()
    while day not in days and day != 'all':
        day = input('\nThat was not a valid selection. Please enter a day from the following: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All.\n').lower().strip()

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
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Frequent Month:', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Frequent Day of the Week:', popular_day)

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    pop_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', pop_start_station)

    # display most commonly used end station
    pop_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', pop_end_station)

    # display most frequent combination of start station and end station trip
    df['start and stop'] = df['Start Station'] + ' and ' + df['End Station']
    pop_start_stop = df['start and stop'].mode()[0]
    print('Most Popular Combination of Start and End Stations:', pop_start_stop)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    if 'Trip Duration' in df.columns:
        # display total travel time
        print('Total Travel Time: {}.'.format(dt.timedelta(seconds = df['Trip Duration'].sum().item())))
        # display mean travel time
        print('Average Travel Time: {} minutes.'.format(df['Trip Duration'].mean()/60))
    else:
        print('\nTrip duration data was not provided for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns:
        user_types = df['User Type'].value_counts()
        print('\nUser Types:\n', user_types)
    else:
        print('\nUser Type data was not provided for this city.')

    # Display counts of gender
    if 'Gender' in df.columns:
        genders = df['Gender'].fillna('Not Provided').value_counts()
        print('\nUser Genders:\n', genders)
    else:
        print('\nUser Gender data was not provided for this city.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nEarliest Birth Year:', df['Birth Year'].min())
        print('\nMost Recent Birth Year:', df['Birth Year'].max())
        print('\nMost Common Birth Year:', df['Birth Year'].mode()[0])
    else:
        print('\nUser Birth Year data was not provided for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
	view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no.\n').lower().strip()
	start_loc = 0
	while (view_data == 'yes'):
		print(df.iloc[start_loc:start_loc+5])
		start_loc += 5
		view_data = input("Do you wish to view the next 5 rows of individual data? Enter yes or no.\n").lower().strip()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower().strip()
        if restart != 'yes':
            break


if __name__ == "__main__":
	main()
