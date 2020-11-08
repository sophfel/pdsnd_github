import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
 

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!!!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    
    while True: 
        city = input("Would you like Chicago, New York City or Washington? ").lower().strip()
    
        if city in CITY_DATA:     
            print('You chose {}'.format(city))
            break
 
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
        month = input('Would you like to filter by month? If so please type the month, if not type all ').lower().strip()
        if month in months:
            print('You chose to show {}'.format(month))
            break
            
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']
        day = input('Would you like to filter by day? If so please type, if not type all ').lower().strip()
        if day in days:
            print('You chose to show {} '.format(day))
            break
     
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
    
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])   
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['journey'] = df['Start Station'] + ' - ' + df['End Station']

    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    while (view_data == 'yes'):
        print(df.iloc[0:4])
        start_loc += 5
        view_data = input('Do you wish to continue?: ')
          
    if month != 'all':
        month = MONTHS.index(month) + 1
        df = df[df['month'] == month]
        
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

    
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    popular_month =df['month'].mode()[0] -1 
    print('The most popular month is ' + MONTHS[popular_month])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour, ': 00')
    popular_day =df['day_of_week'].mode()[0]
    print('The most popular day of the week is ' + popular_day)
    
    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_start = df['Start Station'].mode()[0]
    df['Start Station'].value_counts()
    print('The most popular start station is ' + popular_start)

    popular_end = df['End Station'].mode()[0]
    print('The most popular end station is ' + popular_end)

    print('The most popular journey is ' + df['journey'].mode()[0])
    print(df.columns)
   
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df): 
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total= round((df['Trip Duration'].sum()/60/60)/24, 1)
    print('The total travel time was ' + total.astype(str) + ' days')
   
    averageof = round(df.describe()['Trip Duration'][1]/60, 1)
    print('The average travel time was ' + averageof.astype(str) + ' minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def user_stats(df):
    """Displays statistics on bikeshare users."""
   
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    user_types = df['User Type'].value_counts()
    print('\nTypes of users:\n')
    print(user_types)
   
    checkgen = 'Gender' in df
    if checkgen == True:
        gender = df['Gender'].value_counts()
        print('\nGender of the users:\n')
        print(gender)
            
    checkyear = 'Birth Year' in df
    if checkyear == True:
    
        common_year = df[('Birth Year')].mode()[0]
        print('\nThe most common year of birth is:',int(common_year))
    
        earliest_year = (df['Birth Year'].dropna())
        print('\nThe earliest year of birth is:',int(earliest_year.sort_values().iloc[0]))

        recent_year = (df['Birth Year'].dropna())
        print('\nThe most recent year of birth is:',int(recent_year.sort_values().iloc[-1]))

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
     while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
