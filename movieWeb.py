from flask import Flask, render_template, request
import pandas as pd
from movieInfo import movie_df, metascore_int_coverter, movie_option_selector

app = Flask(__name__)

@app.route("/")
def layout():
    return render_template('index.html')

@app.route("/preferences", methods=["GET", "POST"])
def choices():
    years = movie_df['year'].unique()
    genres = movie_df['genre'].unique()
    metascores = ["Doesn't matter", 'Greater than 50', 'Greater than 60', 'Greater than 70', 'Greater than 80', 'Greater than 90']
    if request.method == "POST":
        year = int(request.form.get('years')) #requests gets users input and stores them into the variables
        genre = request.form.get('genres')
        metascore = request.form.get('metascores')
        metascore = metascore_int_coverter(metascore)
        movie_options = movie_option_selector(year, metascore, genre)
        movie_list = [rows[0] for rows in movie_options] #row[0] returns just the name of the movie
        poster_list = [rows[6] for rows in movie_options] #row[6] returns the link to the poster
        metascore_list = [rows[5] for rows in movie_options] #row[5] returns the metascore of the movie
        if len(movie_list) > 0: #If there are items in the list that means that there are movies to display. Other wise we direct the user to noMovie.html
            return render_template('movieList.html', item_list=zip(movie_list,poster_list, metascore_list))
        else:
            return render_template('noMovie.html')
    return render_template('preferences.html', years=years, genres=genres, metascores=metascores)


if __name__ == "__main__":
   app.run(debug=True)