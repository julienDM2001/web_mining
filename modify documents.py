import pandas as pd

df1 = pd.read_csv("top_500_tmdb/movie_rate.txt")
print(df1.head())
df2 = pd.read_csv("movies.csv")


#for each movieid in df1, take it's int value add one and find the line in df2 with that value
#then add the title to a new column in df1
df1['title'] = df1['movieid'].apply(lambda x: df2.iloc[x-1]['title'])
print(df1.head())
#write the new df1 to the file
df1.to_csv("top_500_tmdb/movie_rate.txt", index=False)