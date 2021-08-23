import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}
months = ['January', 'February', 'March', 'April', 'May', 'June']
days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', ' sunday']


def display_data(df):
    """ Display 7 lines of data  7 rows of data as much as the user wants"""

    view_data = input('\nWould you like to view 7 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while view_data == 'yes':
        if start_loc + 7 <= len(df):
            print(df.iloc[start_loc:start_loc+7])
            start_loc += 7
            view_data = input("Do you wish to continue? Enter yes or no: ").lower()
        else:
            # in case of out of range
            diff = len(df) - start_loc
            if diff == 0:
                print('\nThe end: No more data to display')
                break
            elif diff > 0:
                print(df.iloc[start_loc:start_loc + diff])
                print('\nThe end: No more data to display')
                break


def read_month():
    """
        Asks user to chose a month.

        Returns:
            (int) index of the month
    """
    while True:
        month = input("\nWhich month:"
                      "\n1-January \n2-February \n3-March \n4-April \n5-May \n6-June"
                      "\nPlease enter the month name: ").lower()
        if month == 'january':
            return 1
        elif month == 'february':
            return 2
        elif month == 'march':
            return 3
        elif month == 'april':
            return 4
        elif month == 'may':
            return 5
        elif month == 'june':
            return 6
        else:
            print("\nInvalid input! please try again\n")


def read_day():
    """
        Asks user to chose a day.

        Returns:
            (str) name of the day
    """
    while True:
        day = input("\nWhich day: "
                    "\n1-Monday \n2-Tuesday \n3-Wednesday \n4-Thursday \n5-Friday \n6-Saturday \n7-Sunday"
                    "\nEnter the day name: ").lower()
        if day in days_of_week:
            return day.title()
        else:
            print("\nInvalid number! please try again\n")


def convert_second(seconds):
    """
    Convert seconds into days, hours, minutes and seconds

     Args:
        (int) seconds - time in seconds
     Returns:
        (tuple) days, hours, minutes, seconds
    """
    minutes, seconds = divmod(seconds, 60)
    if minutes >= 60:
        hours, minutes = divmod(minutes, 60)
        if hours >= 24:
            days, hours = divmod(hours, 24)
        else:
            days = 0
    else:
        hours = 0
        days = 0

    return round(days), round(hours), round(minutes), round(seconds)


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data! \U0001F603 \n')
    # get user input for city (chicago, new york city, washington).
    while True:
        city = input("Would you like to see data for:\n "
                     "1-Chicago \n 2-New York \n 3-Washington"
                     "\nPlease enter the city name: ").lower()
        if city in CITY_DATA.keys():
            break
        else:
            print("\nInvalid city name! please try again\n")
    # get user input for filter
    while True:
        filter_data = input("\nWould you like to filter the data by: "
                            "\n1-month \n2-day \n3-both \n4-none"
                            "\nEnter the number corresponding to the filter:").lower()
        if filter_data == 'month':
            # get user input for month (all, january, february, ... , june)
            month = read_month()
            day = 'all'
            break
        elif filter_data == 'day':
            # get user input for day of week (all, monday, tuesday, ... sunday)
            day = read_day()
            month = 'all'
            break
        elif filter_data == 'both':
            # get user input for month (all, january, february, ... , june)
            month = read_month()
            # get user input for day of week (all, monday, tuesday, ... sunday)
            day = read_day()
            break
        elif filter_data == 'none':
            month = 'all'
            day = 'all'
            break
        else:
            print("\nYou entered invalid input! please try again\n")

    print('-' * 100)
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
    # I used pandas 1.2.1: it use dt.day_name() instead of  dt.weekday_name
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    print('-' * 100)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('The most common month:', months[int(popular_month) - 1])
    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('The most common day of week:', popular_day_of_week)
    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('The most common hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 100)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station:', popular_start_station)
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station:', popular_end_station)
    # display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + " - " + df['End Station']
    popular_combination_station = df['combination'].mode()[0]
    print('The most most frequent combination of start station and end station trip:', popular_combination_station)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 100)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total trip number
    print("Total trip number:", df['Trip Duration'].count())

    # display total travel time
    days, hours, minutes, seconds = convert_second(df['Trip Duration'].sum())
    print("Total travel time: {} days : {} hours : {} minutes : {} seconds".format(days, hours, minutes, seconds))

    # display mean travel time
    days, hours, minutes, seconds = convert_second(round(df['Trip Duration'].mean()))
    print("Mean travel time: {} days : {} hours : {} minutes : {} seconds".format(days, hours, minutes, seconds))

    # display min travel time
    days, hours, minutes, seconds = convert_second(df['Trip Duration'].min())
    print("Min travel time: {} days : {} hours : {} minutes : {} seconds".format(days, hours, minutes, seconds))

    # display max travel time
    days, hours, minutes, seconds = convert_second(df['Trip Duration'].max())
    print("Max travel time: {} days : {} hours : {} minutes : {} seconds".format(days, hours, minutes, seconds))

    # Display trip duration  by gender
    print("\nTrip duration by gender:")
    try:
        users_duration_gender = df.groupby(['Gender'])['Trip Duration'].sum()
        days, hours, minutes, seconds = convert_second(users_duration_gender.iloc[0])
        print("Female: {} days : {} hours : {} minutes : {} seconds".format(days, hours, minutes, seconds))
        days, hours, minutes, seconds = convert_second(users_duration_gender.iloc[1])
        print("Male: {} days : {} hours : {} minutes : {} seconds".format(days, hours, minutes, seconds))
    except:
        print("Sorry, there is no data!")

    # Display trip duration  by user types
    print("\nTrip duration by user types:")
    try:
        users_duration_types = df.groupby(['User Type'])['Trip Duration'].sum()
        days, hours, minutes, seconds = convert_second(users_duration_types.iloc[0])
        print("Customer: {} days : {} hours : {} minutes : {} seconds".format(days, hours, minutes, seconds))
        days, hours, minutes, seconds = convert_second(users_duration_types.iloc[1])
        print("Subscriber: {} days : {} hours : {} minutes : {} seconds".format(days, hours, minutes, seconds))
    except:
        print("Sorry, there is no data!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 100)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("\nCounts of user types:")
    try:
        users_type = df.groupby(['User Type'])['User Type'].count()
        print(users_type)
    except:
        print("Sorry, there is no data!")

    # Display counts of gender
    print("\nCounts of user gender:")
    try:
        users_gender = df.groupby(['Gender'])['Gender'].count()
        print(users_gender)
    except:
        print("Sorry, there is no data!")

    # Display average Birth Year for each gender
    print("\nAverage Birth Year for each gender:")
    try:
        users_avr_birth_gender = round(df.groupby(['Gender'])['Birth Year'].mean())
        print(users_avr_birth_gender)
    except:
        print("Sorry, there is no data!")

    # Display earliest, most recent, and most common year of birth
    try:
        print("\nThe earliest birth year:", int(df['Birth Year'].min()))
    except:
        print("\nSorry, there is no Birth Year data!")

    try:
        print("The most recent birth year:", int(df['Birth Year'].max()))
    except:
        print("\nSorry, there is no Birth Year data!")

    try:
        print("The most common birth year:", int(df['Birth Year'].mode()[0]))
    except:
        print("\nSorry, there is no Birth Year data!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 100)


def main():
    while True:
        city, month, day = get_filters()

        if month != 'all':
            print('***** Filters:  City: {} * Month:{} * Day:{} *****'
                  .format(city.title(), months[int(month) - 1], day))
        else:
            print('***** Filters:  City: {} * Month:{} * Day:{} *****'
                  .format(city.title(), month, day))

        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("exit ... \n Good bye  \U0001F603")
            break


if __name__ == "__main__":
    main()
