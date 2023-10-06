import pandas as pd
import numpy as np

df2 = pd.read_csv("links.csv")



df = pd.read_csv("ratings.csv")

# replace the movieId with the TmdbID store in df2
df['movieId'] = df['movieId'].replace(df2.set_index('movieId')['tmdbId'])
# calculte the average ratings for each movie and sort them in descending order
df = df.groupby('movieId').agg({'rating': [np.size, np.mean]})
df = df.sort_values([('rating', 'mean')], ascending=False)
print(df.head(500))



