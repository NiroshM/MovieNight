import csv
import pandas as pd


path = r"C:\Users\Nirosh\Documents\Programming Projects\movie_data.csv"

movie_df = pd.read_csv(path, index_col=False)

#This keeps only the first genre listed for each row in the genre column
genres = list(movie_df['genre'])
genres = [genre.strip().split(",") for genre in genres ]
genres = [item[0] for item in genres]

# This replaces the old genre series with the updated one
movie_df2 = pd.DataFrame({'genre': genres})
movie_df['genre'] = movie_df2['genre']


#FUNCTIONS FOR movieData.py

def metascore_int_coverter(metascore):
    if metascore == "Doesn't matter":
        metascore = 0
    elif metascore == "Greater than 50":
        metascore = 50
    elif metascore == "Greater than 60":
        metascore = 60
    elif metascore == "Greater than 70":
        metascore = 70
    elif metascore == "Greater than 80":
        metascore = 80
    else:
        metascore = 90

    return metascore

def movie_option_selector(year, metascore, genre):
    criteria1 = movie_df['year'] >= year
    criteria2 = movie_df['metascore'] > metascore
    criteria3 = movie_df['genre'] == genre
    criteria = criteria1 & criteria2 & criteria3
    movie_options = movie_df[criteria].values #values gives just the info of the movie without the index or heading
    return movie_options
    




