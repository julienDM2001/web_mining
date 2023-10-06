import pandas as pd

movies = pd.read_csv("movies.csv")

# find the most popular genre for each decade
def find_most_popular_genre(movies):
    """Find the most popular genre for each decade"""
    # create a dictionary with decade as key and a list of genre as value
    dict_genre = {}
    for i in movies.iterrows():
        # find the year of the movie store between the parentheses in the title
        # if the following condition cannot be transform into int then continue


        try:
            year = i[1].title[i[1].title.find("(")+1:i[1].title.find(")")]
            decade = int(year) - int(year) % 10
        except:
            continue
        # transform the year into a decade

        # find the genre of the movie
        genre = i[1]["genres"].split("|")
        if decade not in dict_genre:
            dict_genre[decade] = genre
        else:
            dict_genre[decade] += genre

    # find the most popular genre for each decade
    dict_most_popular_genre = {}
    for decade in dict_genre:
        dict_most_popular_genre[decade] = max(set(dict_genre[decade]), key = dict_genre[decade].count)
    # transform dict_genre to have a count of each genre by decade
    for decade in dict_genre:
        dict_genre[decade] = {i:dict_genre[decade].count(i) for i in dict_genre[decade]}

    return dict_most_popular_genre,dict_genre

dict_most_popular_genre,genre = find_most_popular_genre(movies)
print(dict_most_popular_genre,genre)