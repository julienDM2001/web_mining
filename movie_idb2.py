import pandas as pd

links_df = pd.read_csv("links.csv")
#generate a matrix with the tmbid for each pair of movieId imbId
def generate_matrix(links_df):
    """Generate a matrix with the tmbid for each pair of movieId imbId"""
    matrix = []
    for index, row in links_df.iterrows():
        matrix.append([row["movieId"], row["tmdbId"]])
    return matrix
matrix = generate_matrix(links_df)
print(matrix)
