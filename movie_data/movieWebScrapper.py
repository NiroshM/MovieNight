#All imports
from requests import get
from bs4 import BeautifulSoup
from time import sleep
from random import randint
from IPython.core.display import clear_output
import pandas as pd

#Makes a dataframe using the data collected
def makeDataFrame(names_list, years_list, view_ratings_list, genres_list, imdb_list, metascore_list, poster_list):
    dataframe = pd.DataFrame({  'movie': names_list,
                                'year': years_list,
                                'view rating' : view_ratings_list,
                                'genre' : genres_list,
                                'IMDb rating' : imdb_list,
                                'metascore' : metascore_list,
                                'posters' : poster_list
                                })
    dataframe['year'] = dataframe['year'].str[-5:-1].astype(int)
    dataframe['genre'] = dataframe['genre'].str[1:]

    return dataframe

def main():
    #Lists to iterate through to switch the url year and page number
    years_url = [str(i) for i in range(2000, 2019)]
    pages = ['0', '51', '101', '151']

    #Lists that will store the movie data
    names = []
    years = []
    view_ratings = []
    genres = []
    imdb_ratings = []
    metascores = []
    poster_links = []

    numRequests = 0

    for year_url in years_url:
    
        for page in pages:
        
            url = 'https://www.imdb.com/search/title?release_date={}-01-01,{}-12-31&sort=num_votes,desc&start={}&ref_=adv_prv'.format(year_url, year_url, page)
            response = get(url)
        
            #Pause the loop anywhere from 8 to 15 seconds
            sleep(randint(8, 15))
        
            numRequests += 1
            print('Request: {}'.format(numRequests))
            clear_output(wait = True)

            html_soup = BeautifulSoup(response.text, 'html.parser')
    
            movie_containers = html_soup.find_all('div', class_ = 'lister-item mode-advanced')
    
            for movie in movie_containers:
            
                if movie.find('div', class_ = 'ratings-metascore') != None:
                    #Add name of movie to names list
                    name = movie.h3.a.text
                    names.append(name)

                    #Add year of movie to years list
                    year = movie.h3.find('span', class_ = 'lister-item-year').text
                    years.append(year)
                
                    #Add the legal view rating to the view ratings list
                    view_rating = movie.p.span.text
                    view_ratings.append(view_rating)
                
                    #Add genre to the genres list
                    genre = movie.p.find('span', class_ = 'genre').text
                    genres.append(genre)
                
                    #Add imdb rating to imdb ratings list
                    imdb_rating = float(movie.strong.text) 
                    imdb_ratings.append(imdb_rating)
        
                    #Add metascore to metascores list
                    metascore = movie.find('span', class_ = 'metascore').text
                    metascores.append(int(metascore))

                    #Add poster link to the poster links list
                    poster_link = movie.a.img.get('loadlate')
                    poster_links.append(poster_link)

    movie_data = makeDataFrame(names, years, view_ratings, genres, imdb_ratings, metascores, poster_links)
    movie_data.to_csv('movie_data.csv', index = False)

if __name__ == "__main__":
    main()