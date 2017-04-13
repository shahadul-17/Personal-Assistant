import pandas as pd

column_names = ['user_id','item_id','rating','timestamp']
ratings = pd.read_csv('C:/Users/ashik/Documents/GitHub/Personal-Assistant/Server/data/recommenderdata/u.data',sep='\t',names=column_names)
print(ratings.head())
movie_titles = pd.read_csv('C:/Users/ashik/Documents/GitHub/Personal-Assistant/Server/data/recommenderdata/Movie_Id_Titles')
print(movie_titles.head())
ratings = pd.merge(ratings,movie_titles,on='item_id')
print(ratings.head())
print(ratings.groupby('title')['rating'].mean())
movie_matrix = ratings.pivot_table(index = 'user_id',columns = 'title',values = 'rating')
print(movie_matrix.head())

starwarsrating = movie_matrix['Star Wars (1977)']
print(starwarsrating.head())

