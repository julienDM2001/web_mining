import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import bs4
import requests
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import seaborn as sns
from typing import List, Dict
import codecs

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

# DORYAN
link = pd.read_csv("./links.csv")
print(link.head())
movie = pd.read_csv("./movies.csv")
print(movie.head())
ratings = pd.read_csv("./ratings.csv")

tags = pd.read_csv("./tags.csv")


class Actor:
    """
    This class represents an actor.

    |

    The instance attributes are:

    actor_id:
        Identifier of the actor.

    name:
        Name of the actor.

    movies:
        List of movies in which the actor has played.
    """

    # -------------------------------------------------------------------------
    actor_id: int
    name: str
    movies: List["Movie"]

    # -------------------------------------------------------------------------
    def __init__(self, actor_id: int, name: str):
        """
        Constructor.

        :param actor_id: Identifier of the actor.
        :param name: Name of the actor.
        """

        self.actor_id = actor_id
        self.name = name
        self.movies = []


class Movie:
    """
    This class represents a movie_to_analyse.

    |

    The instance attributes are:

    movie_id:
        Identifier of the movie_to_analyse.

    name:
        Name of the movie_to_analyse in the IMDb database.

    actors:
        List of actors who have played in the movie_to_analyse.

    summary:
        Summary of the movie_to_analyse.
    """

    # -------------------------------------------------------------------------
    movie_id: int
    name: str
    actors: List[Actor]
    summary: str

    # -------------------------------------------------------------------------
    def __init__(self, movie_id: int, name: str):
        """
        Constructor.

        :param movie_id: Identifier of the movie_to_analyse.
        :param name: Name fo the movie_to_analyse.
        """

        self.movie_id = movie_id
        self.name = name
        self.actors = []
        self.summary = ""

    def __repr__(self):
        return "For info movie class is made up of {} movie_id, {} name, {} actors, {} summary \n".format(self.movie_id,
                                                                                                          self.name,
                                                                                                          self.actors,
                                                                                                          self.summary)


class Parser:
    genre_list = dict()
    main_genre = dict()
    score_film = dict()
    """

    |

    The instance attributes are:

    output:
        Directory where to store the resulting data.

    basic_url:
        Begin of the URL used to retrieve the HTML page of a movie_to_analyse.

    actors:
        Dictionary of actors (the identifiers are the key).

    actors:
        Dictionary of actors (the names are the key).

    movies:
        Dictionary of movies (the identifiers are the key).
    """

    # -------------------------------------------------------------------------
    output: str
    basic_url: str
    actors: Dict[int, Actor]
    actors_by_name: Dict[str, Actor]
    movies: Dict[int, Movie]

    # -------------------------------------------------------------------------
    def __init__(self, output: str, basic_url: str) -> None:
        """
        Initialize the parser.

        :param output: Directory where to store the results.
        :param basic_url: Beginning part of the URL of a movie_to_analyse page.
        """

        self.output = output + os.sep
        if not os.path.isdir(self.output):
            os.makedirs(self.output)
        self.basic_url = basic_url
        self.actors = dict()
        self.actors_by_name = dict()
        self.movies = dict()
        self.genre = list()

    # -------------------------------------------------------------------------
    def extract_data(self, movie: str) -> None:
        """
        Extract the "useful" data from the page. In practice, the following steps are executed:

        1. Build the URL of the movie_to_analyse page.

        2. Create a new Movie instance and add it to the list.

        3. Download the HTML page and use an instance of BeautifulSoup to parse.

        4. Extract all "div" tags and analyze those of the class "summary_text" (summary of the movie_to_analyse) and
        "credit_summary_item" (directors, producers, actors, etc.).

        :param movie: Analyzed movie_to_analyse.
        """
        print(movie)
        url = self.basic_url + movie

        doc_id = movie
        movie = Movie(doc_id, movie)
        self.movies[doc_id] = movie

        # Download the HTML using the requests library, check the status-code and extract the text
        ## @COMPLETE : use the requests library here, get the response and extract the content

        response = requests.get(url, headers=headers)
        content = response.content

        # Download the HTML and parse it through Beautifulsoup
        soup = bs4.BeautifulSoup(content, "html.parser")

        # Extract infos
        self.extract_summary(movie, soup)
        self.extract_actors(movie, soup)
        self.extract_genre(movie, soup)
        self.extract_score(movie, soup, doc_id)

    # -------------------------------------------------------------------------
    def extract_summary(self, movie, soup) -> None:
        """
        This function extract the summary from a movie/tv-show
        It use the find_all method of BeautifulSoup to find the "overview" class
        """
        divs = soup.find_all("div")
        for div in divs:
            div_class = div.get("class")
            if div_class is not None:
                if 'overview' in div_class:
                    movie.summary = div.text

    def extract_score(self, movie, soup, doc_id) -> None:
        """
        This function extract the score from a movie/tv-show
        It use the find_all method of BeautifulSoup to find the "ratingValue" class
        """
        divs = soup.find_all("div")
        for div in divs:
            div_class = div.get("class")
            if div_class is not None:
                if 'user_score_chart' in div_class:
                    # get the calue store in data-percent in the div
                    score = div.get("data-percent")

                    Parser.score_film[doc_id] = score

    # -------------------------------------------------------------------------
    def extract_actors(self, movie, soup) -> None:
        """
        This function extract the list of actors displayed for a specific movie/tv-show
        It use the select method of BeautifulSoup to extract actors displayed on the page.
        Actor are defined in people scroller cards
        """

        soup_results = soup.select("ol[class='people scroller'] li[class='card'] p a")
        actors = [soup_result.text for soup_result in soup_results]

        # Store actors in class dictionaries
        for actor in actors:
            if actor not in self.actors_by_name.keys():
                actor_id = len(self.actors) + 1  # First actor_id = 1
                new_actor = Actor(actor_id, actor)
                self.actors[actor] = new_actor
                self.actors_by_name[actor] = new_actor
            self.actors_by_name[actor].movies.append(movie)
            movie.actors.append(self.actors_by_name[actor])

    def extract_genre(self, movie, soup) -> None:
        """this function extract the genre of a movie/tv-show and store it in a dictionary with the movie_id as key"""
        divs = soup.find_all("div")
        for div in divs:
            div_class = div.get("class")

            if div_class is not None:
                if 'facts' in div_class:
                    for span in div.find_all('span'):
                        if "genres" in span.attrs['class']:
                            split_text = span.get_text(strip=True)
                            Parser.genre_list[movie.movie_id] = split_text + "\n"
                            new_split = split_text.split(",")

                            Parser.main_genre[movie.movie_id] = new_split[0] + "\n"

    # -------------------------------------------------------------------------
    def write_files(self) -> None:
        """
        Write all the file. Three thinks are done:

        1. For each document, create a file (doc*.txt) that contains the summary and the name of
        the actors.

        2. Create a CSV file "actors.txt" with all the actors and their identifiers.

        3. Build a matrix actors/actors which elements represent the number of times
        two actors are playing in the same
        movie_to_analyse.

        4. Create a CSV file "links.txt" that contains all the pairs of actors having played together.
        """

        # Write the clean text
        for movie in self.movies.values():
            if len(movie.actors) < 2:
                continue
            movie_file = codecs.open(self.output + 'doc_' + str(movie.movie_id) + ".txt", 'w', "utf-8")
            movie_file.write(movie.summary + "\n")

        # Write the list of actors
        actors_file = codecs.open(self.output + "actors.txt", 'w', "utf-8")
        for actor in self.actors.values():
            actors_file.write(str(actor.actor_id) + ',"' + actor.name + '"\n')

        # Build the matrix actors/actors
        matrix = np.zeros(shape=(len(self.actors), len(self.actors)))
        for movie in self.movies.values():
            for i in range(0, len(movie.actors) - 1):
                for j in range(i + 1, len(movie.actors)):
                    # ! Matrix begins with 0, actors with 1
                    matrix[movie.actors[i].actor_id - 1, movie.actors[j].actor_id - 1] += 1
                    matrix[movie.actors[j].actor_id - 1, movie.actors[i].actor_id - 1] += 1

        # Write only the positive links
        links_file = codecs.open(self.output + "links.txt", 'w', "utf-8")
        for i in range(0, len(self.actors) - 1):
            for j in range(i + 1, len(self.actors)):
                weight = matrix[i, j]
                if weight > 0.0:
                    # ! Matrix begins with 0, actors with 1
                    links_file.write(str(i + 1) + "," + str(j + 1) + "," + str(weight) + "\n")

        # find the top 500 movies in Parser.score and store them in top_500_tmdb directory
        actor_500 = []
        if dir_docs == "docs/":
            top_500 = sorted(Parser.score_film.items(), key=lambda x: x[1], reverse=True)[:500]
            for i, j in top_500:
                movie_file = codecs.open("top_500_tmdb/doc_" + str(i) + ".txt", 'w', "utf-8")
                movie_file.write(str(self.movies[i].summary) + "\n")
                actor_file = codecs.open("top_500_tmdb/actors.txt", 'a', "utf-8")
                for i in self.movies[i].actors:
                    actor_file.write(str(i.actor_id) + ',"' + i.name + '"\n')
                    if i.actor_id not in actor_500:
                        actor_500.append(i.actor_id)

            # create the link between the 500 best film actors
            links_file = codecs.open("top_500_tmdb/links.txt", 'w', "utf-8")

            for i in range(len(matrix)):
                for y in range(i + 1, len(matrix[i])):
                    if i in actor_500 and y in actor_500:
                        if matrix[i][y] > 0:
                            links_file.write(str(i) + "," + str(y) + "," + str(matrix[i][y]) + "\n")
            # create the genre file for the best 500 film
            for i, j in top_500:
                movie_file = codecs.open("top_500_tmdb/movie_rate" + ".txt", 'a', "utf-8")
                genre_file = codecs.open("top_500_tmdb/movie_genre" + ".txt", 'a', "utf-8")
                movie_file.write(str(i) + (",") + str(j) + "\n")
                genre_file.write(str(i) + (",") + str(Parser.genre_list[i]) + "\n")

            genre_file = codecs.open(self.output + "genre.txt", 'w', "utf-8")
            for movie in Parser.genre_list:
                genre_file.write(str(movie) + "," + str(Parser.genre_list[movie]))

            main_genre_file = codecs.open(self.output + "main_genre.txt", 'w', "utf-8")
            for movie in Parser.genre_list:
                main_genre_file.write(str(movie) + "," + str(Parser.main_genre[movie]))

            # in the different film_by_genre directory write the movie summary in the corresponding genre directory

            for movie in Parser.genre_list:
                genre = Parser.genre_list[movie]
                # find the directory corresponding to the genre
                for directory in os.listdir("film_by_genre"):
                    if directory in genre:
                        # write the summary in the corresponding genre directory
                        movie_file = codecs.open("film_by_genre/" + directory + "/doc_" + str(movie) + ".txt", 'w',
                                                 "utf-8")
                        movie_file.write(self.movies[movie].summary + "\n")

        if dir_docs == "top_500/":
            genre_file = codecs.open(self.output + "genre.txt", 'w', "utf-8")
            for movie in Parser.genre_list:
                genre_file.write(str(movie) + "," + str(Parser.genre_list[movie]))

            main_genre_file = codecs.open(self.output + "main_genre.txt", 'w', "utf-8")
            for movie in Parser.genre_list:
                main_genre_file.write(str(movie) + "," + str(Parser.main_genre[movie]))

            # in the different film_by_genre directory write the movie summary in the corresponding genre directory
            for movie in Parser.genre_list:
                genre = Parser.genre_list[movie]
                # find the directory corresponding to the genre
                for directory in os.listdir("film_by_genre"):
                    if directory in genre:
                        # write the summary in the corresponding genre directory
                        movie_file = codecs.open("film_by_genre/" + directory + "/doc_" + str(movie) + ".txt", 'w',
                                                 "utf-8")
                        movie_file.write(self.movies[movie].summary + "\n")







list_name = []
list_id = []
for i in movie.title:
    list_name.append(i)
for y in link.tmdbId:
    list_id.append(str(y))
list_movies = list(zip(list_name, list_id))

new_list_movie = list_movies[0:100]
# ----------------------------------------------------------------------------------------
# Initialize a list of movies to download
basic_url_to_analyze = 'https://www.themoviedb.org/movie/'
dir_docs = "./doc2"

# -----------------------------------------------------------------------------------------
# Use our custom parser to download each HTML page and save the actors and the links
parser = Parser(dir_docs, basic_url_to_analyze)
for movie_label, movie_id in new_list_movie:
    parser.extract_data(movie_id)
parser.write_files()
print(Parser.score_film)