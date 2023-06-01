#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import pandas as pd
import numpy as np
from tabulate import tabulate


# In[2]:


def get_filters(city_data):
    """
    Here you have to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington)
    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington? ').lower()
        if city in city_data:
            break
        else:
            print('Invalid city. Please choose from Chicago, New York City, or Washington.')
    
    # Get user input for month (all, january, february, ..., june)
    month = input('Which month? Enter a month name (e.g., January) or "all" for all months: ').lower()
    
    # Get user input for day of week (all, monday, tuesday, ..., sunday)
    day = input('Which day of the week? Enter a day of the week (e.g., Monday) or "all" for all days: ').lower()
    
    print('-' * 40)
    return city, month, day


# In[3]:


def load_data(city, month, day, city_data):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (dict) city_data - dictionary containing the city data filenames

    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load data file for the specified city
    filename = city_data[city]
    df = pd.read_csv(filename)

    # Convert the 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month, day, and hour from the 'Start Time' column to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour

    # Filter by month if applicable
    if month != 'all':
        # Convert month name to month number
        month = month.lower()
        month_num = ['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1
        df = df[df['Month'] == month_num]

    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['Day of Week'] == day.title()]

    return df


# In[4]:


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    common_month = df['Month'].mode()[0]
    month_name = ['January', 'February', 'March', 'April', 'May', 'June'][common_month - 1]
    print('Most Common Month:', month_name)
    
    # Display the most common day of week
    common_day = df['Day of Week'].mode()[0]
    print('Most Common Day of Week:', common_day)
    
    # Display the most common start hour
    common_hour = df['Hour'].mode()[0]
    print('Most Common Start Hour:', common_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


# In[5]:


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most Commonly Used Start Station:', common_start_station)
    
    # Display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most Commonly Used End Station:', common_end_station)
    
    # Display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
    common_trip = df['Trip'].mode()[0]
    print('Most Frequent Trip:', common_trip)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


# In[6]:


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel_time, 'seconds')
    
    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time:', mean_travel_time, 'seconds')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


# In[7]:


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of User Types:\n', user_types)
    
    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('\nCounts of Gender:\n', gender_counts)
    else:
        print('\nGender information is not available for this dataset.')
    
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode()[0])
        print('\nEarliest Birth Year:', earliest_birth_year)
        print('Most Recent Birth Year:', most_recent_birth_year)
        print('Most Common Birth Year:', common_birth_year)
    else:
        print('\nBirth year information is not available for this dataset.')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


# In[8]:


def display_raw_data(df):
    """Displays 5 lines of raw data upon request by the user."""
    i = 0
    while True:
        display_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        if display_data.lower() != 'yes':
            break
        print(tabulate(df.iloc[i:i+5], headers="keys", showindex=False))
        i += 5


# In[9]:


def main():
    CITY_DATA = {
        'chicago': 'chicago.csv',
        'new york city': 'new_york_city.csv',
        'washington': 'washington.csv'
    }
    
    while True:
        city, month, day = get_filters(CITY_DATA)
        df = load_data(city, month, day, CITY_DATA)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == '__main__':
    main()

