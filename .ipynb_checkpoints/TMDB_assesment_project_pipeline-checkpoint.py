# %%
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

# %%
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# %%


# %% [markdown]
# # Extracting the Data from an API about about movies TMDB

# %%
import requests
from pprint import pprint

movie_genres_url = "https://api.themoviedb.org/3/genre/movie/list?language=en"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhYzI4NmYzODdkNzkzYzliYzRkOWNmOTU0MDY5OWY5NyIsInN1YiI6IjY1N2RhZGRkYzkwNTRmMDcwMWI1MTQ5MSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.UjWYoaCdhkZX1IcDA3pI7XzJAviiAJ64X5-Tn_Sv6xQ"
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


# %%
# converting the orginal data and the genre data to a dataframe
df= pd.DataFrame(all_movies)
genres_df=pd.DataFrame(genres)
genres_df.set_index(keys="id")
df.head(2)

# %% [markdown]
# # Transforming the Data 
# 

# %%
# transforming the genre_ids column into a new column with genre names
def get_genre_names(ids):
    matching_genres = genres_df[genres_df["id"].isin(ids)]
    return list(matching_genres["name"])

get_genre_names([80, 18, 36])

# %%
df['genre_name'] = df['genre_ids'].apply(get_genre_names)
df['genre_name']

# %%
# tranforming the genre_name column into a string
def list_to_str(lst):
        return  ','.join(lst)
print(df['genre_name'].apply(list_to_str))
df['genre_name']= df['genre_name'].apply(list_to_str)
print(df['genre_name'])

# %%
#trnasforming the type of date column into a date type

df['release_date']= pd.to_datetime(df['release_date'])

# %%
# transforming the release date column and creating a column for year and a column for month

df['year'] = df['release_date'].dt.year
df['month'] = df['release_date'].dt.month

# %%


# %%
# droping columns that won't be used
df = df.drop('adult', axis=1)
df = df.drop('backdrop_path', axis=1)
df = df.drop('poster_path', axis=1)
df = df.drop('video', axis=1)
df = df.drop('genre_ids', axis=1)

# %%
#creating a column for legnth of titles for future maniuplation 
df['title_legnth']=[len(title) for title in df['original_title']] 


# %%
df.head(1)

# %% [markdown]
# # Load Data into csv and Sql database 
# 

# %%
df.to_csv('tmdb_project.csv')

# %%
import sqlite3
con = sqlite3.connect('db')
df.to_sql('tmdb_project',con, if_exists='replace')


# %%
pd.read_sql_query('select * from tmdb_project',con)

# %%


# %%


# %% [markdown]
# # Maiuplationg and aggregating the data and visualizing it 

# %%
# what are the months that has the most movies releases?

# %%


df['month'] = df['release_date'].dt.month_name()

agg = df['month'].value_counts()

agg = agg.reindex([
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
])

plt.figure(figsize=(10, 6))
sns.barplot(x=agg.index, y=agg.values, palette="viridis")


plt.title('Monthly Distribution of Releases')
plt.xlabel('Month')
plt.ylabel('Number of Releases')
plt.xticks(rotation=45, ha='right') 


plt.show()

# %%


# %%
# what is the average voting for movies per each year

# %%

avg_voting_per_year = df.groupby('year')['vote_average'].sum().reset_index()

avg_voting_per_year

# %%
# distrubution of languages of movies
languages = df.groupby('original_language').size()
languages.plot(kind='pie',figsize=(10, 6))
plt.legend()
plt.show()

# %%


# %%
#what is the most popular movie in the past 10 years
most_popular_movie = df[['original_title','release_date','genre_name']][df['popularity']== df['popularity'].max()]
most_popular_movie

# %%
# what is the most comon genre split in the past 10 years?
genre_counts = df['genre_name'].str.split(',').explode().value_counts().reset_index()
genre_counts.columns = ['genre', 'count']

top_genres = genre_counts.head(5)
sns.barplot(x=top_genres['genre'], y = top_genres['count'])
plt.show()

# %%
from matplotlib.animation import FuncAnimation
#plt.barh(top_genres['genre'],top_genres['count'])
fig,ax= plt.subplots()
plt.xlim(0,130)
plt.gca().invert_yaxis()
plt.rcParams["font.family"] = "helvetica"
ax.set_xlabel('number of movies') 
ax.set_ylabel('Genres') 
ax.set_title("The distripution of most popular genres")
ax.spines['right'].set_visible(False) 
ax.spines['top'].set_visible(False) 
ax.spines['bottom'].set_visible(False)
plt.barh(top_genres['genre'], top_genres['count'], color=['#FF4C00', '#007749', '#C8102E', '#002C5F', '#910BF3'])

def init():
    plt.barh(top_genres['genre'], [0,0,0,0,0])
    
def animate(i):
    plt.barh(top_genres['genre'], top_genres['count'] * i / 100, color=['#FF4C00', '#007749', '#C8102E', '#002C5F', '#910BF3'])
    
anim = FuncAnimation(fig, animate, init_func=init, repeat=True, save_count=100)
anim.save('100mPretty.gif', writer='imagemagick', fps=10, dpi=240)


# %%


# %% [markdown]
# ### which year saw the most vote count for movies? 
# 

# %%
avg_yearly_vote_count =df.groupby('year')['vote_count'].mean().reset_index()

ax = sns.barplot(x=avg_yearly_vote_count['year'] , y= avg_yearly_vote_count['vote_count'])
ax.bar_label(ax.containers[0], fontsize=10)
plt.show()

# %%


# %% [markdown]
# ### Movie with the longest title?

# %%
longest_title_movies = df[['title','release_date','genre_name','title_legnth']].sort_values('title_legnth', ascending=False)
longest_title_movies.head()

# %%


# %%


# %%


# %%



