import streamlit as st
import pandas as pd
import pickle
import requests
import numpy as np


file =  r'D:\Venkatesh\Projects\Recommend system\Content Based Rec\Pycharm\venv\Movies'
# movies_dict = pickle.load(open( r'D:\Venkatesh\Projects\Recommend system\Content Based Rec\Pycharm\venv\Movies\data_dict_7.6k.pkl','rb'))
# movies = pd.DataFrame(movies_dict)

movies = pd.read_csv(r'D:\Venkatesh\Projects\Recommend system\Content Based Rec\Pycharm\venv\Movies\data2 (1).csv')


similarity = pickle.load(open(r'D:\Venkatesh\Projects\Recommend system\Content Based Rec\Pycharm\venv\Movies\Similarity_final_edition.pkl','rb'))
# https://www.omdbapi.com/?i=tt3896198&apikey=a9a9a557

def fetch_poster(movie_id):
    api_key = "a9a9a557"  # Replace with your actual OMDB API key
    url = 'https://www.omdbapi.com/?i={}&apikey={}'.format(movie_id, api_key)
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        poster_url = data.get('Poster')
        return poster_url
    else:
        print("Error: Failed to fetch data from the OMDB API.")
        return None

# Recommendation function
def recommend_movies(movie_name, similarity_matrix, movie_data, top_n=10):
    # Convert the user input to lowercase
    movie_name = movie_name.lower()

    if movie_name not in movie_data['title'].str.lower().values:
        return "Movie not found in the database."

    movie_index = movie_data[movie_data['title'].str.lower() == movie_name].index[0]
    similarity_scores = similarity_matrix[movie_index]

    # Find the indices of the top similar movies (excluding the input movie itself)
    similar_movie_indices = np.argsort(similarity_scores)[::-1][1:top_n + 1]

    # Get movie titles based on the indices
    recommended_movies = [movie_data.iloc[idx]['title'] for idx in similar_movie_indices]

    return recommended_movies


# Streamlit web application

# Streamlit web application
st.title('Movie Recommender System of Venkatesh')

# Define your selectbox to choose the movie
selected_movie_name = st.selectbox(
    'What movie are you interested in',
    movies['title'].values)

# Check if the "Recommend" button is clicked
if st.button('Recommend'):
    recommendations = recommend_movies(selected_movie_name, similarity, movies)

    if isinstance(recommendations, str):
        st.error(recommendations)  # Display an error message if the movie is not found
    else:
        num_recs = len(recommendations)  # All recommendations

        # Display two movies in a row with space between them and expander buttons
        for i in range(0, num_recs, 2):
            col1, col2 = st.columns(2)

            for j in range(2):
                if i + j < num_recs:
                    recommended_movie = recommendations[i + j]
                    movie_data = movies[movies['title'] == recommended_movie].iloc[0]
                    movie_poster_url = fetch_poster(movie_data['imdb_id'])

                    with col1 if j == 0 else col2:
                        # Display movie poster with a larger width
                        st.image(movie_poster_url, width=340)



                        # Add custom spacing using HTML
                        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

                        # Add space between two movie columns
                        st.markdown("<div style='width: 20px;'></div>", unsafe_allow_html=True)

                        # Create an expander button to show additional information
                        expander = st.expander(f' More Info  -   *********{recommended_movie}*********')

                        with expander:
                            st.subheader('Overview')
                            st.write(movie_data['overview'])

                            st.subheader('Lead Actors')
                            st.write(movie_data['actor'])

                            st.subheader('Director')
                            st.write(movie_data['director'])

                            st.subheader('Genre')
                            st.write(movie_data['genre_names'])






