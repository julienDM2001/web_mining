import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


df = pd.read_csv("tags.csv")
print(df.head())


#function that create a dictionary with user_id key and the list of tag as value
def create_dict(df):
    """Create a dictionary with user_id as key and the list of tag as value"""
    dict_movie = {}
    for index, row in df.iterrows():
        if row["userId"] not in dict_movie:
            dict_movie[row["userId"]] = [row["tag"]]
        else:
            dict_movie[row["userId"]].append(row["tag"])
    return dict_movie
x = create_dict(df.sort_values(by = "userId"))

#function that creates a graph with the weight between two user as the number of tag in commun
def transform_to_graph(x):
    """Transform the x dictionary in a graph with the weight between two user as the number of tag in commun"""
    g = nx.Graph()
    for user in x:
        g.add_node(user)
    for user1 in x:
        for user2 in x:
            if user1 != user2:
                g.add_edge(user1, user2, weight = len(set(x[user1]).intersection(set(x[user2]))))
    return g

# function that create a dictionary with userId as key and the list of movieId as value
def create_dict_movie(df):
    """Create a dictionary with userId as key and the list of movieId as value"""
    dict_user = {}
    for index, row in df.iterrows():
        if row["userId"] not in dict_user:
            dict_user[row["userId"]] = [row["movieId"]]
        else:
            dict_user[row["userId"]].append(row["movieId"])
    return dict_user
#transfor the dict_user in a graph with the weight between two user as the number of movie in commun
def transform_to_graph_movie(x):
    """Transform the x dictionary in a graph with the weight between two user as the number of movie in commun"""
    g = nx.Graph()
    for user in x:
        g.add_node(user)
    for user1 in x:
        for user2 in x:
            if user1 != user2:
                if len(set(x[user1]).intersection(set(x[user2]))) > 0:
                    g.add_edge(user1, user2, weight = len(set(x[user1]).intersection(set(x[user2]))))
    return g

g = transform_to_graph(x)
nx.write_gml(g, "graph/tag_graph.gml")
x2 = create_dict_movie(df.sort_values(by = "userId"))
g2 = transform_to_graph_movie(x2)
nx.write_gml(g2, "graph/movie_graph.gml")