import streamlit as st
import pickle
import pandas as pd
import requests


st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0f0f1a 0%, #1a0f2e 50%, #0f1a0f 100%); }
    
    .hero { text-align: center; padding: 3rem 0 2rem; }
    .hero h1 { font-size: 3rem; font-weight: 600;
                background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                margin-bottom: 0.5rem; }
    .hero p { color: #888; font-size: 1.1rem; font-weight: 300; }

    div[data-baseweb="select"] > div {
        background-color: #1a1a2e !important;
        border: 1px solid #555 !important;
        border-radius: 12px !important;
    }
    div[data-baseweb="select"] span {
        color: white !important;
        font-size: 1rem !important;
    }
    div[data-baseweb="popover"] li {
        background-color: #1a1a2e !important;
        color: white !important;
    }
    div[data-baseweb="popover"] li:hover {
        background-color: #2a2a4e !important;
    }

    .stButton > button {
        background: linear-gradient(90deg, #7c3aed, #2563eb) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2.5rem !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        width: 100% !important;
    }
    .stButton > button:hover { opacity: 0.85 !important; }

    .movie-card {
        background: #1a1a2e;
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid #2a2a4a;
        margin-bottom: 1rem;
    }
    .movie-card:hover { transform: translateY(-4px); transition: transform 0.2s; }
    .info { padding: 0.75rem; }
    .rank { color: #a78bfa; font-size: 0.75rem; text-align: center; margin-bottom: 4px; }
    .title { color: #e2e8f0; font-size: 0.85rem; font-weight: 500; text-align: center; }
    .no-poster { background: #1a1a2e; height: 280px; display: flex;
                 align-items: center; justify-content: center;
                 color: #444; font-size: 3rem; }
    .section-title { color: #a78bfa; font-size: 1.1rem; font-weight: 500;
                     margin: 2rem 0 1rem; letter-spacing: 0.05em; text-transform: uppercase; }

    footer, #MainMenu, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

API_KEY = st.secrets["TMDB_API_KEY"]

def fetch_poster(movie_id, title):
    # Try by movie_id first
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
        data = requests.get(url, timeout=5).json()
        if data.get('poster_path'):
            return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
    except:
        pass

    # Fallback — search by title
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}"
        data = requests.get(url, timeout=5).json()
        if data['results'] and data['results'][0].get('poster_path'):
            return f"https://image.tmdb.org/t/p/w500{data['results'][0]['poster_path']}"
    except:
        pass

    return None

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    names, posters = [], []
    for i in movie_list:
        title = movies.iloc[i[0]].title
        movie_id = movies.iloc[i[0]].id
        names.append(title)
        posters.append(fetch_poster(movie_id, title))  # pass both
    return names, posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.markdown("""
<div class="hero">
    <h1>Movie Recommendation</h1>
    
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    selected_movie = st.selectbox("", movies['title'].values, label_visibility="collapsed")
    clicked = st.button("Find Similar Movies")

if clicked:
    with st.spinner("Finding perfect matches..."):
        names, posters = recommend(selected_movie)

    st.markdown('<div class="section-title">✦ Recommended for you</div>', unsafe_allow_html=True)

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.markdown('<div class="movie-card">', unsafe_allow_html=True)
            if posters[idx]:
                st.image(posters[idx], use_container_width=True)
            else:
                st.markdown('<div class="no-poster">🎬</div>', unsafe_allow_html=True)
            st.markdown(f"""
                <div class="info">
                    <div class="rank">#{idx+1} Pick</div>
                    <div class="title">{names[idx]}</div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)