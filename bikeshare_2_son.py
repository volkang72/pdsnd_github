import time
import pandas as pd
import numpy as np
import pprint


CITY_DATA = { 'chicago': 'C:/Users/TCVGAZIOGLU/Desktop/DATA SCIENCE/chicago.csv',
              'new york city': 'C:/Users/TCVGAZIOGLU/Desktop/DATA SCIENCE/new_york_city.csv',
              'washington': 'C:/Users/TCVGAZIOGLU/Desktop/DATA SCIENCE/washington.csv' }

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
    while True:
        print('\nWould you like to see data for Chicago, New York City or Washington')
        city = input().strip().lower()
        if city not in ('chicago', 'new york city', 'washington'):
            print('\nPlease, type the city correctly')
        else:
            break

    while True:
        print('\nWould you like to filter data by "month", "day", "both" or not at all? Type "none" for no time filter.')
        data_filter = input().strip().lower()
            
        if data_filter == 'none':
            month, day = 'all', 'all'
            break
        
    # get user input for month (all, january, february, ... , june)
        
        elif data_filter == 'month':
            print('\nWhich month? January, February, March, April, May, or June?')
            while True:
                month = input().strip().lower()
                if month not in ('january', 'february', 'march', 'april', 'may', 'june'):
                    print('\nPlease, type "month" correctly!')
                else:
                    day = 'all'
                    break   
            break
    # get user input for day of week (all, monday, tuesday, ... sunday) 
                
        elif data_filter == 'day':  
            print('\nWhich day? Monday, Tuesday, ... Sunday')
            while True:
                day = input().strip().lower()
                if day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
                    print('Please, type "day" correctly!')
                else:
                    month = 'all'
                    break
            break
    # get user input for month (all, january, february, ... , june) and day of week (all, monday, tuesday, ... sunday)               
        elif data_filter == 'both':
            print('\nWhich month? January, February, March, April, May, or June?')
            while True:
                month = input().strip().lower()
                if month not in ('january', 'february', 'march', 'april', 'may', 'june'):
                    print('\nPlease, type "month" correctly!')
                else:
                    break  
                
            print('\nWhich day? Monday, Tuesday, ... Sunday')    
            while True:
                day = input().strip().lower()
                if day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
                    print('\nPlease, type "day" correctly!')
                else:
                    break
            break
    
        else:
        
            print('\nPlease, type correct data filter!')
            
    print('-'*40)
    return city, month, day, data_filter


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    df = df.rename(columns = {'Unnamed: 0' : 'Index'})

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'all':
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df, month, day, datafilter):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    print('<Filter: {}>'.format(datafilter.title()))
    start_time = time.time()
    # display the most common month
    if month == 'all':
        monthly_count = df['month'].value_counts()
        print('Most popular month:      {:<10}      Total count: {:^6,} out of {:^6,}'.format(monthly_count.index[0].upper(), monthly_count.iloc [0], df['month'].count()))
  
    # display the most common day of week
    if day == 'all':
        day_of_week_count = df['day_of_week'].value_counts()
        print('Most popular day:        {:<10}      Total count: {:^6,} out of {:^6,}'.format(day_of_week_count.index[0].upper(), day_of_week_count.iloc [0], df['day_of_week'].count()))
    
    # display the most common start hour
    start_hour_count = df['Start Time'].dt.hour.value_counts()
    print('Most popular start hour: {:<10}      Total count: {:^6,} out of {:^6,}'.format(start_hour_count.index[0], start_hour_count.iloc[0], df['Start Time'].count()))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, datafilter):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    print('<Filter: {}>'.format(datafilter.title()))
    start_time = time.time()

    # display most commonly used start station
    start_station_count = df['Start Station'].value_counts()
    print('Most popular Start Station : {:^70}  Total Count: {:<6,}'.format(start_station_count.index[0].upper(), start_station_count.iloc[0]))
        
    # display most commonly used end station
    end_station_count = df['End Station'].value_counts()
    print('Most popular End Station :   {:^70}  Total Count: {:<6,}'.format(end_station_count.index[0].upper(), end_station_count.iloc[0]))
        
    # display most frequent combination of start station and end station trip
    df['Route'] = df['Start Station'] + ' <-> ' +  df['End Station']
    route_count = df['Route'].value_counts()
    print('Most popular trip route :    {:^70}  Total Count: {:<6,}'.format(route_count.index[0].upper(), route_count.iloc[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, datafilter):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    print('<Filter: {}>'.format(datafilter.title()))
    start_time = time.time()

    # display total travel time
    total_trip_duration = np.sum(df['Trip Duration'])
    print('Total trip duration: {}'.format(pd.to_timedelta(total_trip_duration, unit='s')))
    
    # display mean travel time
    mean_trip_duration = np.mean(df['Trip Duration'])
    print('Total trip duration: {}'.format(pd.to_timedelta(mean_trip_duration, unit='s')))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, datafilter):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User type statistics...\n')
    print('<Filter: {}>'.format(datafilter.title()))
    user_type_count = df['User Type'].value_counts()
    user_type_percent = df['User Type'].value_counts(normalize= True)
    user_type_list = user_type_count.index.tolist()   
    for i in range(len(user_type_list)):
        print('{:<10}        Total Count: {:<8,}        Percentage: {:<4.2%}'.format(user_type_count.index[i], user_type_count[i], user_type_percent[i]))

    # Display counts of gender
    print('\nGender statistics...\n')
    print('<Filter: {}>'.format(datafilter.title()))
    if 'Birth Year' in df.columns.values.tolist():    
        gender_count = df['Gender'].value_counts(dropna=False)
        gender_percent = df['Gender'].value_counts(dropna=False, normalize= True)
        gender_list = gender_count.index.tolist()   
        for i in range(len(gender_list)):
            print('{:<8}       Total Count: {:<8,}           Percentage: {:.2%}'.format(gender_count.index[i], gender_count[i], gender_percent[i]))
    else:
        print('No gender data available!\n')
        
    # Display earliest, most recent, and most common year of birth
    print('\nUser year of birth statistics...\n')
    print('<Filter: {}>'.format(datafilter.title()))
    if 'Birth Year' in df.columns.values.tolist():
        min_year = int(df['Birth Year'].min())
        max_year = np.max(df['Birth Year'])
        most_common_year= df['Birth Year'].mode()[0]
        print('Earliest year of birth :    {:.0f}\nRecent year of birth :      {:.0f}\nMost common year of birth : {:.0f}'.format(min_year, max_year, most_common_year))
    
    else:
        print('No year of birth data available!\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def individual_data_view(df):
    """Displays individual user data."""
        
    n, m = 0, 5
    while True:
        start_time = time.time()
        
        print('Would you like to view individual trip data? Type "yes" or "no" to continue.')
        choice = input().strip()
        print('\nDisplaying individual user data...\n')
        if  choice.lower() not in ('yes', 'no'):
            print('Please type it carefully!')
        else:
            if choice.lower() == 'no':
                print('Thanks for the investigation of the Bikeshare data & statistics.')
                break
            else:
                if m < df.shape[0]:                
                    for i in range(n,m):
                        pprint.pprint(df.iloc[i])
                        n += 1
                        m += 1
                        print('.'*60)
                else:
                    break
                
        print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40) 

def main():
    while True:
        city, month, day, data_filter = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day, data_filter)
        station_stats(df, data_filter)
        trip_duration_stats(df, data_filter)
        user_stats(df, data_filter)
        individual_data_view(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
                                
        
if __name__ == "__main__":
	main()
