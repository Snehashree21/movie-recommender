# Movie Recommender System

A content-based movie recommender system built with Python and Streamlit.

## Live Demo
🔗 [Click here to try the app](https://movie-recommender-v1.streamlit.app/)

## About
It recommends movies similar to your selected movie using Natural Language Processing and Cosine Similarity. It fetches real movie posters from the TMDB API.

## How it works
- Select a movie from the dropdown
- Click "Find Similar Movies"
- Get 5 movie recommendations with posters

## Tech Stack
- **Python** — core language
- **Pandas** — data processing
- **Scikit-learn** — cosine similarity
- **NLTK** — text vectorization
- **Streamlit** — web app framework
- **TMDB API** — movie posters

## Dataset
Uses the TMDB 5000 Movies dataset from Kaggle containing 5000 movies.

## Installation

Clone the repository:
```bash
git clone https://github.com/Snehashree21/movie-recommender.git
cd movie-recommender
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Add your TMDB API key in `.streamlit/secrets.toml`:
```toml
TMDB_API_KEY = "your_api_key_here"
```

Run the app:
```bash
streamlit run App.py
```

## Screenshots
<img width="892" height="422" alt="image" src="https://github.com/user-attachments/assets/3a84baee-04f6-4faa-b5b6-aed2476bdaba" />


## Author
Made by Snehashree
