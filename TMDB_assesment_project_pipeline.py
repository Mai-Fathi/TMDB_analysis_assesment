import pandas as pd 
import sqlite3
from api_key import api_key
################################################################
# Extracting the Data from an API about about movies TMDB

import requests
movie_genres_url = "https://api.themoviedb.org/3/genre/movie/list?language=en"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer " + api_key
}

def get_movies_for_year(year):
    url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc&primary_release_year=" + str(year)
    response = requests.get(url, headers=headers).json()["results"]
    return response

years = [2013,2014,2015,2016,2017,2018,2019,2020,2023]
years_movies = list(map(get_movies_for_year, years))

all_movies = []

for year_movies in years_movies:
    all_movies = all_movies + year_movies
    
genres = requests.get(movie_genres_url, headers=headers).json()['genres']


################################################################
# Transforming the Data 

# converting the orginal data and the genre data to a dataframe
df= pd.DataFrame(all_movies)
genres_df=pd.DataFrame(genres)
genres_df.set_index(keys="id")

# transforming the genre_ids column into a new column with genre names
def get_genre_names(ids):
    matching_genres = genres_df[genres_df["id"].isin(ids)]
    return list(matching_genres["name"])

df['genre_name'] = df['genre_ids'].apply(get_genre_names)
df['genre_name']

# tranforming the genre_name column into a string
def list_to_str(lst):
        return  ','.join(lst)
df['genre_name']= df['genre_name'].apply(list_to_str)

#trnasforming the type of date column into a date type

df['release_date']= pd.to_datetime(df['release_date'])

# transforming the release date column and creating a column for year and a column for month

df['year'] = df['release_date'].dt.year
df['month'] = df['release_date'].dt.month

# droping columns that won't be used
df = df.drop('adult', axis=1)
df = df.drop('backdrop_path', axis=1)
df = df.drop('poster_path', axis=1)
df = df.drop('video', axis=1)
df = df.drop('genre_ids', axis=1)

#creating a column for legnth of titles for future maniuplation 
df['title_legnth']=[len(title) for title in df['original_title']] 

################################################################

# Load Data into csv and Sql database 

df.to_csv('tmdb_project.csv')

con = sqlite3.connect('db')
df.to_sql('tmdb_project',con, if_exists='replace')




