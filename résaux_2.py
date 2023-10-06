
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
import codecs



df = pd.read_csv("docs/links.txt")

# list_actor = []
# for i in df["actor1"]:
#     if i not in list_actor:
#         list_actor.append(i)
# for i in df["actor2"]:
#     if i not in list_actor:
#         list_actor.append(i)
# list_actor.append(0)
# #trier actor en ordre croissant
# list_actor.sort()


top_500_actors = pd.read_csv("top_500/links.txt")
list_500_actors = []
for i in top_500_actors["actor1"]:
    if i not in list_500_actors:
        list_500_actors.append(i)
for i in top_500_actors["actor2"]:
    if i not in list_500_actors:
        list_500_actors.append(i)


# représenter un résaux d'acteur avec un graphe ou les poids sont le number_of_commune_movies entre deux acteurs
def transform_to_graph(df,list_actor):
    """Transform the df dataframe in a graph with the weight between two actor as the number of film in commun"""
    g = nx.Graph()
    for actor in list_actor:
        g.add_node(actor)
    for index, row in df.iterrows():
        if row["number_of_common_movies"] > 0:
            g.add_edge(row["actor1"], row["actor2"], weight = row["number_of_common_movies"])
    return g

# x = transform_to_graph(df,list_actor)
# nx.write_gml(x, "graph/graph.gml")
#
# df1 = pd.read_csv("text_analysis/cosine_similarity_TF_IDF.txt")
#
# y = transform_to_graph(top_500_actors,list_500_actors)
#
# nx.write_gml(y, "graph/top_500_actors.gml")

top_500_tmdb_actor = pd.read_csv("top_500_tmdb/links.txt")
print(top_500_tmdb_actor.head())
list_500_tmdb = []
for i in top_500_tmdb_actor["actor1"]:
    if i not in list_500_tmdb:
        list_500_tmdb.append(i)
for i in top_500_tmdb_actor["actor2"]:
    if i not in list_500_tmdb:
        list_500_tmdb.append(i)
g = transform_to_graph(top_500_tmdb_actor,list_500_tmdb)
nx.write_gml(g, "graph/top_500_tmdb_actors.gml")
