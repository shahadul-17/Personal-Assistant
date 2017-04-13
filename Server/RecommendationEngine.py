import pandas

class RecommendationEngine:

column_names = [ 'user_id', 'item_id', 'rating', 'timestamp' ]

ratings = pandas.read_csv(".\\data\\u.data", sep='\t', names=column_names, encoding='latin-1')
print(ratings.head())
movie_titles = pandas.read_csv(".\\data\\Movie_Id_Titles")
print(movie_titles.head())
ratings = pandas.merge(ratings, movie_titles, on='item_id')
print(ratings.head())
# print(ratings.groupby('title')['rating'].mean())
movie_matrix = ratings.pivot_table(index = 'user_id', columns = 'title', values = 'rating')
# print(movie_matrix.head())

starwarsrating = movie_matrix['Star Wars (1977)']
print(starwarsrating.head())

#Reading items file:
i_cols = ['movie id', 'movie title' ,'release date','video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure',
 'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
items = pandas.read_csv(".\\data\\u.item", sep='|', names=i_cols, encoding='latin-1')
print(items.head())