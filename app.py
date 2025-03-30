import pickle
import streamlit as st
import requests

OMDB_API_KEY = 'df697186 ' # Replace with your OMDb API Key


def fetch_poster(movie_name):
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()

        print(f"🔍 IMDb API Response for {movie_name}: {data}")  # Debugging log

        poster_url = data.get("Poster")  # Fetch IMDb poster URL safely
        if poster_url and poster_url != "N/A":
            print(f"✅ Poster Found: {poster_url}")
            return poster_url
        else:
            print(f"⚠️ No poster available for {movie_name}")
            return "https://via.placeholder.com/500x750?text=No+Image"

    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        return "https://via.placeholder.com/500x750?text=Error+Fetching+Image"


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_name = movies.iloc[i[0]].title
        recommended_movie_names.append(movie_name)

        poster_url = fetch_poster(movie_name)  # Fetch IMDb poster
        recommended_movie_posters.append(poster_url)

    return recommended_movie_names, recommended_movie_posters


st.header('Movie Recommender System')

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)

    for idx, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[idx])
            st.image(recommended_movie_posters[idx])
