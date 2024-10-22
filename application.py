import pickle
import streamlit as st
import requests

# Function to fetch the poster from TMDb
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Function to recommend movies based on similarity
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Streamlit app
st.header('Movie Recommender System')

# Load movie data and similarity matrix
movies = pickle.load(open('movies1.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Add a selectbox for users to choose a movie
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

# Button to show recommendations
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

# Option to update and save new movie data or similarity matrix
st.sidebar.header("Admin Options")
new_movies = None

# Button to update and save movie data
if st.sidebar.button('Update Movie Data'):
    # Example of how to update `new_movies` (Replace with actual data logic)
    new_movies = movies  # In actual implementation, `new_movies` could be a modified DataFrame

    # Save the updated movie data and similarity matrix
    pickle.dump(new_movies, open('movies1.pkl', 'wb'))
    pickle.dump(similarity, open('similarity.pkl', 'wb'))

    st.sidebar.success("Movie data and similarity matrix saved successfully!")
