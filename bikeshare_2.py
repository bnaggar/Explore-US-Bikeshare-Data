import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("\nWhich city would you like to analyze?\n").strip().title()

    while city not in ['Chicago', 'New York City', 'Washington']:
        print("Invalid input! Please, choose between(Chicago, New York City, Washington).")
        city = input("\nWhich city would you like to analyze?\n").strip().title()

    print("The city name is:", city)


    # get user input for month (all, january, february, ... , june)
    month = input("\nWhich month would you like to filter by?\n").strip().title()

    while month not in ['January', 'February', 'March', 'April', 'May', 'June', 'All']:
        print("Invalid input! Please, choose between(January, February, March, April, May, June, All).")
        month = input("\nWhich month would you like to filter by?\n").strip().title()

    print("The month is:", month)


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("\nWhich day would you like to filter by?\n").strip().title()

    while day not in ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'All']:
        print("Invalid input! Please, choose between(Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, All).")
        day = input("\nWhich day would you like to filter by?\n").strip().title()

    print("The day is:", day)

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
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print("The most common month is:", common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print("The most common week day is:", common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print("The most common start hour is:", common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("The most common start station is:", common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("The most common end station is:", common_end_station)

    # display most frequent combination of start station and end station trip
    common_start_end_station = (df['Start Station'] + " - " + df['End Station']).mode()[0]
    print("The most frequent start station and end station trip is:", common_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = round(df['Trip Duration'].sum())
    print("Total travel time is:", total_travel_time)

    # display mean travel time
    mean_travel_time = round(df['Trip Duration'].mean())
    print("Mean travel time is:", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts().to_frame()
    print("User types are:\n", user_types)

    # Display counts of gender
    try:
        gender_types = df['Gender'].value_counts().to_frame()
        print("\nGender types are:\n", gender_types)
    except KeyError:
        print("\nThere's no gender types data available for Washington.\n")


    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = int(df['Birth Year'].min())
        print("\nThe earliest birth year is:", earliest_birth_year)
    except KeyError:
        print("There's no birth year data available for Washington.")

    try:
        latest_birth_year = int(df['Birth Year'].max())
        print("The latest birth year is:", latest_birth_year)
    except KeyError:
        print("There's no birth year data available for Washington.")

    try:
        common_birth_year = int(df['Birth Year'].mode()[0])
        print("The most common birth year is:", common_birth_year)
    except KeyError:
        print("There's no birth year data available for Washington.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """Asks the user whether they want to display the raw data"""

    while True:
        try:
            raw_data = input("\nWould you like to display the raw data? Please, choose between(Yes, No).\n").strip().title()
            if raw_data == 'Yes':
                display_data = df.sample(5)
                print(display_data)
            elif raw_data == 'No':
                break
        except ValueError:
            print("Invalid input! Please, choose between(Yes, No).")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Please, choose between(Yes, No).\n').strip().title()
        if restart != 'Yes':
            break


if __name__ == "__main__":
	main()