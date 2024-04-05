import streamlit as st
import pickle
import requests

movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

API_KEY = '48800aee0ea8f4ab2acd3ca475c368d9'
BASE_URL = "https://api.themoviedb.org/3"

# function to recommend similar movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    for i in distance[1:6]:
        recommend_movie.append(movies.iloc[i[0]].title)
    return recommend_movie

# Function to fetch movie details 
def fetch_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {
        'api_key': API_KEY,
        'append_to_response': 'credits'  
    }
    response = requests.get(url, params=params)
    movie_data = response.json()
    return movie_data

#page design
st.set_page_config(
    page_title="Cinegram",
    page_icon="🎬",
    layout="wide"
)

st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6; 
    }
    .stApp {
        background-image: url('https://assets-global.website-files.com/5fa4da31b6c3a45d2cfd2d5d/61e96f3699c067827896210e_Sundance%202022%20-%2010%20DC%20picks%20-%20Hero.jpeg');
        background-size: cover;
        background-repeat: no-repeat;
        filter: brightness(.9);
    }
    .sidebar .sidebar-content {
        background-color: rgba(255, 255, 255, 0.5);
        box-shadow: 0px 0px 10px 5px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
    }
    .st-ba {
        background-color: rgba(255, 255, 255, 0.5);
        box-shadow: 0px 0px 10px 5px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("CINEGRAM")
st.header("A Movie Surfer....")
selectvalue = st.selectbox("Select Movies From Dropdown List", movies_list)

# Display recommendations when button is clicked
if st.button("Show recommend"):
    movie_names = recommend(selectvalue)
    cols = st.columns(5)  
    for idx, movie_name in enumerate(movie_names):
        url = f"{BASE_URL}/search/movie"
        params = {
            'api_key': API_KEY,
            'query': movie_name
        }
        response = requests.get(url, params=params)
        data = response.json()
        if 'results' in data and len(data['results']) > 0:
            movie_info = data['results'][0]
            poster_path = movie_info['poster_path']
            movie_id = movie_info['id']
            if poster_path:
                movie_data = fetch_movie_details(movie_id)
                poster_url = f"https://image.tmdb.org/t/p/original{poster_path}"
                movie_link = f"https://www.themoviedb.org/movie/{movie_id}"
                overview = movie_data['overview']
                rating = movie_data['vote_average']
                cast = ", ".join(actor['name'] for actor in movie_data['credits']['cast'][:5])  # Get first 5 cast members
                cols[idx].image(poster_url, caption=movie_name, use_column_width=True)
                cols[idx].markdown(f"**Overview:** {overview}\n\n"
                                   f"**Rating:** {rating}\n\n"
                                   f"**Cast:** {cast}\n\n"
                                   f"[{movie_name} on TMDb]({movie_link})", unsafe_allow_html=True)
