import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']

month_list = ['all','january','february','march','april','may','june']

days_list = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']

city_list = ['chicago', 'new york city' ,'washington']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # gets user input for the city
    
    city = input("Please Enter Name Of a City: ").lower()
    
    while city not in city_list:
        city = input("Please Choose Between Chicago,New York City,Washington ")
        
        
    # get user input for month (all, january, february, ... , june)
    month = input("Please Enter a Month: ").lower()
    
    
    while month not in month_list:
        month = input("Please Enter a Month like january,february,...june or all: ")
        
        
    # gets user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please Enter a day :").lower()
    
    while day not in days_list:
        day = input("Please enter a day like Sunday,Monday...etc or type all for all days : ")
                 
            
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
    # loading csv files in to df
    df = pd.read_csv(CITY_DATA[city])

   # converts start time and end time columns in to YYYY-MM-DD Format using to_datetime method
    df["Start Time"] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    #extract month from Start Time into new column called month
    
    df['month'] = df['Start Time'].dt.month

    #filter by month

    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # extract day from Start Time into new column called month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #  display the most common month
    print("Most common month is :", df['month'].value_counts().idxmax())


    #  display the most common day of week
    print("Most common day is :", df['day_of_week'].value_counts().idxmax())

    
    #  display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("Most common hour is :", df['hour'].value_counts().idxmax())

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #  display most commonly used start station
    
    print("Most common start station is :", df['Start Station'].value_counts().idxmax())

    # display most commonly used end station
    print("Most common end station is :", df['End Station'].value_counts().idxmax())

    # display most frequent combination of start station and end station trip
    print("The most frequent combination of start station and end station trip")
    
    most_common_start_end = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print(most_common_start_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum() / 3600.0 
    print('Total traveling time is :',total_duration)

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('Mean travel time is:', mean_time/60, " Minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].count()
    print('user type count is :',user_type)

    
    if city.title() == 'Chicago' or city.title() == 'New York City': # condition to display info for NYC&Chicago
        
        # Display counts of gender
        gender = df['Gender'].count()
        print("The count of gender is: ",gender)

        # Display earliest, most recent, and most common year of birth for the specified data
        earliet_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]
        print('Earliest birth from the data is: ',earliet_year)
        print('Most recent birth from the data is: ',most_recent_year)
        print('Most common birth from the data is: ',most_common_year )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def raw_data (df):
   
    print('Press enter to see raw data, press no to skip')
    x = 0
    while (input()!= 'no'):
        x = x+5 # counter for specifying number of appearing columns&rows
        print(df.head(x)) # to access x as number of rows in the df


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
