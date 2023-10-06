import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
import codecs

top_500 = pd.read_csv("top_500_tmdb/movie_genre.txt")
#function that create a dictionary with movie_id as key and list of genre split on | as value


print(top_500.head())


# fusion the column genre1 to genre 6 in one column with | as separator between each genre if a genre is NaN it is not added to the list
top_500['genre'] = top_500['genre1'].fillna('') + '|' + top_500['genre2'].fillna('') + '|' + top_500['genre3'].fillna('') + '|' + top_500['genre4'].fillna('') + '|' + top_500['genre5'].fillna('') + '|' + top_500['genre6'].fillna('')
print(top_500.head())

# remove all the | if they are  not follow by a genre
top_500['genre'] = top_500['genre'].str.replace(r'\|(?=\|)', '')
# remove all the | at the end of the string
top_500['genre'] = top_500['genre'].str.replace(r'\|$', '')
# remove the column genre1 to genre 6
top_500 = top_500.drop(['genre1', 'genre2', 'genre3', 'genre4', 'genre5', 'genre6'], axis=1)
print(top_500.head())

# create a graph each movie as a node and the number of common genre as weight color each node by it's first genre
G = nx.Graph()
for index, row in top_500.iterrows():
    G.add_node(row['movie'], genre=row['genre'].split('|')[0])
    for index2, row2 in top_500.iterrows():
        if index != index2:
            common_genre = set(row['genre'].split('|')).intersection(set(row2['genre'].split('|')))
            if len(common_genre) > 0:
                G.add_edge(row['movie'], row2['movie'], weight=len(common_genre))
nx.write_gml(G, "graph/movie_500tmdb_genre.gml")

