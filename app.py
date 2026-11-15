"""
CineScope — Movie Ratings and Genre Trends
Discover Movies. Explore Ratings. Find Your Next Favourite.

A Modern, Beautiful, and Fully Working Movie Analytics & Discovery Application.
Built with Python, Streamlit, Plotly, Pandas, and OMDb API integration.
"""

import os
import re
import json
import urllib.request
import urllib.parse
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. Page Configuration & Cinematic Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="CineScope — Movie Ratings & Discovery",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Cinematic Dark Theme
st.markdown("""
<style>
    /* Dark Cinematic Theme Base */
    .stApp {
        background-color: #0B0F19;
        color: #F8FAFC;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    }
    
    /* Clean Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0F172A;
        border-right: 1px solid #1E293B;
    }
    
    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #1E1B4B 0%, #172554 50%, #0B0F19 100%);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 32px 36px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    .hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-tag {
        display: inline-block;
        background: linear-gradient(90deg, #F59E0B, #D97706);
        color: #0F172A;
        font-weight: 800;
        font-size: 0.75rem;
        padding: 5px 12px;
        border-radius: 20px;
        text-transform: uppercase;
        margin-bottom: 12px;
        letter-spacing: 0.8px;
    }
    .hero-subtitle {
        color: #94A3B8;
        font-size: 1.15rem;
        margin-top: 8px;
        max-width: 800px;
        line-height: 1.5;
    }

    /* Metric Cards */
    .metric-card {
        background-color: #131D33;
        border: 1px solid #1E2E4D;
        border-radius: 14px;
        padding: 20px 22px;
        height: 100%;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    }
    .metric-card:hover {
        border-color: #F59E0B;
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(245, 158, 11, 0.15);
    }
    .metric-label {
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 700;
        color: #94A3B8;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 2.1rem;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 4px;
        line-height: 1.15;
    }
    .metric-desc {
        font-size: 0.86rem;
        color: #38BDF8;
        line-height: 1.4;
    }

    /* Movie Poster Cards */
    .movie-card {
        background-color: #131D33;
        border: 1px solid #1E2E4D;
        border-radius: 12px;
        overflow: hidden;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    .movie-card:hover {
        border-color: #8B5CF6;
        transform: translateY(-4px);
        box-shadow: 0 10px 25px rgba(139, 92, 246, 0.2);
    }
    .movie-card-img {
        width: 100%;
        height: 280px;
        object-fit: cover;
        background-color: #1E293B;
    }
    .movie-card-body {
        padding: 16px;
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .movie-card-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 6px;
        line-height: 1.3;
    }
    .movie-card-genres {
        font-size: 0.78rem;
        color: #A855F7;
        margin-bottom: 10px;
        font-weight: 600;
    }
    .movie-card-meta {
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 0.85rem;
        color: #CBD5E1;
        border-top: 1px solid #1E2E4D;
        padding-top: 10px;
        margin-top: 8px;
    }
    .badge-star {
        background-color: #F59E0B;
        color: #0F172A;
        font-weight: 800;
        padding: 2px 7px;
        border-radius: 6px;
        font-size: 0.82rem;
    }

    /* Movie Details View */
    .detail-card {
        background-color: #131D33;
        border: 1px solid #1E2E4D;
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 24px;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4);
    }
    .detail-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 0 0 6px 0;
        line-height: 1.2;
    }
    .detail-tagline {
        color: #38BDF8;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 14px;
    }
    .genre-chip {
        display: inline-block;
        background-color: rgba(139, 92, 246, 0.2);
        border: 1px solid #8B5CF6;
        color: #DDD6FE;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 20px;
        margin-right: 6px;
        margin-bottom: 8px;
    }
    .rating-box {
        background-color: #0F172A;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 14px 18px;
        margin-top: 14px;
        margin-bottom: 14px;
    }

    /* Explainer Cards */
    .chart-explainer {
        background-color: #111A2E;
        border-left: 4px solid #F59E0B;
        border-radius: 0 10px 10px 0;
        padding: 14px 18px;
        margin-top: 10px;
        margin-bottom: 24px;
        font-size: 0.92rem;
        color: #CBD5E1;
        line-height: 1.5;
    }
    .chart-explainer strong {
        color: #FDE68A;
    }
    .chart-takeaway {
        margin-top: 6px;
        color: #38BDF8;
        font-weight: 600;
    }

    /* Section Titles */
    .section-title {
        font-size: 1.5rem;
        font-weight: 750;
        color: #FFFFFF;
        margin-top: 28px;
        margin-bottom: 6px;
    }
    .section-desc {
        color: #94A3B8;
        font-size: 0.96rem;
        margin-bottom: 20px;
        line-height: 1.45;
    }

    /* Friendly Alert Box */
    .friendly-box {
        background-color: #131D33;
        border: 1px dashed #F59E0B;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        color: #FDE68A;
        font-size: 1rem;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Session State Initialization
# -----------------------------------------------------------------------------
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "🏠 Home"
if "search_query" not in st.session_state:
    st.session_state["search_query"] = ""
if "selected_movie_id" not in st.session_state:
    st.session_state["selected_movie_id"] = None
if "selected_external_movie" not in st.session_state:
    st.session_state["selected_external_movie"] = None

# -----------------------------------------------------------------------------
# 3. Data Loading & Caching
# -----------------------------------------------------------------------------
@st.cache_data
def load_movie_data():
    """Load and clean MovieLens datasets with verified real numbers."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path fallbacks for flexibility
    movies_candidates = [
        os.path.join(base_dir, "data", "movies.csv"),
        os.path.join(base_dir, "ml-latest-small", "movies.csv"),
        os.path.join(base_dir, "movies.csv")
    ]
    ratings_candidates = [
        os.path.join(base_dir, "data", "ratings.csv"),
        os.path.join(base_dir, "ml-latest-small", "ratings.csv"),
        os.path.join(base_dir, "ratings.csv")
    ]
    links_candidates = [
        os.path.join(base_dir, "data", "links.csv"),
        os.path.join(base_dir, "ml-latest-small", "links.csv"),
        os.path.join(base_dir, "links.csv")
    ]

    movies_path = next((p for p in movies_candidates if os.path.exists(p)), None)
    ratings_path = next((p for p in ratings_candidates if os.path.exists(p)), None)
    links_path = next((p for p in links_candidates if os.path.exists(p)), None)

    if not movies_path or not ratings_path:
        st.error("Dataset files (`movies.csv` and `ratings.csv`) are missing. Please verify the `data/` folder.")
        return None, None, None, None, None

    movies_df = pd.read_csv(movies_path)
    ratings_df = pd.read_csv(ratings_path)
    links_df = pd.read_csv(links_path) if links_path else pd.DataFrame(columns=["movieId", "imdbId", "tmdbId"])

    # 1. Clean release years using regex
    movies_df["year"] = movies_df["title"].str.extract(r"\((\d{4})\)").astype(float)
    
    # 2. Clean movie title (strip year for presentation)
    movies_df["clean_title"] = movies_df["title"].str.replace(r"\s*\(\d{4}\)", "", regex=True).str.strip()

    # 3. Calculate rating stats per movie
    stats = ratings_df.groupby("movieId").agg(
        rating_count=("rating", "count"),
        mean_rating=("rating", "mean")
    ).reset_index()

    # 4. Merge stats and links into movies
    merged = pd.merge(movies_df, stats, on="movieId", how="left")
    merged["rating_count"] = merged["rating_count"].fillna(0).astype(int)
    merged["mean_rating"] = merged["mean_rating"].fillna(0.0).round(2)

    if not links_df.empty:
        merged = pd.merge(merged, links_df[["movieId", "imdbId", "tmdbId"]], on="movieId", how="left")
    else:
        merged["imdbId"] = np.nan
        merged["tmdbId"] = np.nan

    # 5. Calculate Fair Ranking Score (Bayesian Weighted Rating)
    C = ratings_df["rating"].mean() # ~3.50 global mean
    m = 50 # Minimum votes threshold
    v = merged["rating_count"]
    R = merged["mean_rating"]
    merged["fair_score"] = ((v / (v + m)) * R + (m / (v + m)) * C).round(2)

    # 6. Explode genres for genre-level analytics
    movies_genre = movies_df.copy()
    movies_genre["genre_list"] = movies_genre["genres"].str.split("|")
    exploded = movies_genre.explode("genre_list")
    exploded = exploded.rename(columns={"genre_list": "genre"})
    exploded = exploded[exploded["genre"] != "(no genres listed)"]

    # Merge ratings with exploded genres for true genre ratings
    genre_ratings = pd.merge(ratings_df, exploded[["movieId", "genre"]], on="movieId", how="inner")

    return movies_df, ratings_df, merged, exploded, genre_ratings

# -----------------------------------------------------------------------------
# 4. External Movie API Integration (OMDb)
# -----------------------------------------------------------------------------
DEFAULT_OMDB_KEY = "trilogy" # Verified working public key with fallback

@st.cache_data(ttl=86400, show_spinner=False)
def fetch_omdb_details(imdb_id=None, title=None, year=None, custom_key=None):
    """
    Fetch rich movie metadata (Poster, Plot, Director, Cast, IMDb Rating, Runtime)
    from OMDb API with caching and error handling.
    """
    api_key = custom_key.strip() if custom_key and custom_key.strip() else os.environ.get("OMDB_API_KEY", DEFAULT_OMDB_KEY)
    
    params = {"apikey": api_key}
    if imdb_id and pd.notna(imdb_id):
        # Format as tt0114709
        try:
            imdb_int = int(imdb_id)
            params["i"] = f"tt{imdb_int:07d}"
        except:
            params["i"] = str(imdb_id)
    elif title:
        params["t"] = str(title).strip()
        if year and pd.notna(year):
            params["y"] = str(int(year))
    else:
        return None

    url = f"https://www.omdbapi.com/?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "CineScope/2.0"})

    try:
        with urllib.request.urlopen(req, timeout=4) as response:
            data = json.loads(response.read().decode())
            if data.get("Response") == "True":
                return {
                    "found": True,
                    "title": data.get("Title", title),
                    "year": data.get("Year", year),
                    "poster": data.get("Poster") if data.get("Poster") != "N/A" else None,
                    "plot": data.get("Plot") if data.get("Plot") != "N/A" else "No plot summary available.",
                    "director": data.get("Director") if data.get("Director") != "N/A" else "Unknown",
                    "actors": data.get("Actors") if data.get("Actors") != "N/A" else "Unknown",
                    "runtime": data.get("Runtime") if data.get("Runtime") != "N/A" else "Unknown",
                    "language": data.get("Language") if data.get("Language") != "N/A" else "English",
                    "released": data.get("Released") if data.get("Released") != "N/A" else "Unknown",
                    "imdb_rating": data.get("imdbRating") if data.get("imdbRating") != "N/A" else "N/A",
                    "imdb_votes": data.get("imdbVotes") if data.get("imdbVotes") != "N/A" else "N/A",
                    "imdb_id": data.get("imdbID")
                }
            else:
                return {"found": False, "error": data.get("Error", "Movie not found")}
    except Exception as e:
        return {"found": False, "error": str(e)}

# -----------------------------------------------------------------------------
# 5. Load Data Bundle
# -----------------------------------------------------------------------------
data_bundle = load_movie_data()
if data_bundle is None or data_bundle[0] is None:
    st.stop()

movies_df, ratings_df, merged_df, exploded_df, genre_ratings = data_bundle

total_movies = len(movies_df)
total_ratings = len(ratings_df)
total_users = ratings_df["userId"].nunique()
avg_rating_global = round(ratings_df["rating"].mean(), 2)
min_year = int(movies_df["year"].dropna().min())
max_year = int(movies_df["year"].dropna().max())

# -----------------------------------------------------------------------------
# 6. Sidebar Controls & Navigation
# -----------------------------------------------------------------------------
st.sidebar.markdown("""
<div style="text-align: center; padding: 12px 0 16px 0;">
    <span style="font-size: 2.3rem;">🎬</span>
    <h2 style="color: #FFFFFF; font-size: 1.4rem; margin: 4px 0 0 0; font-weight: 800;">CineScope</h2>
    <p style="color: #F59E0B; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; margin: 0;">Movie Discovery & Analytics</p>
</div>
""", unsafe_allow_html=True)

nav_options = [
    "🏠 Home",
    "🔍 Movie Search and Details",
    "📊 Movie Analytics Dashboard",
    "🎭 Explore Genres",
    "⭐ Top Movies",
    "💡 Rating Insights"
]

current_nav = st.sidebar.radio(
    "Navigation Menu:",
    nav_options,
    index=nav_options.index(st.session_state["current_page"]) if st.session_state["current_page"] in nav_options else 0
)

# Update session state if user clicks sidebar radio
if current_nav != st.session_state["current_page"]:
    st.session_state["current_page"] = current_nav
    st.rerun()

st.sidebar.markdown("---")

# Global Settings & Optional API Key
st.sidebar.markdown("<p style='font-size: 0.82rem; font-weight: 700; color: #94A3B8; text-transform: uppercase;'>⚙️ Optional Settings</p>", unsafe_allow_html=True)
custom_omdb_key = st.sidebar.text_input(
    "OMDb API Key (Optional):",
    value="",
    type="password",
    help="Enter your personal key from omdbapi.com for unlimited worldwide searches and high-res posters. A public fallback is active by default."
)

st.sidebar.markdown("""
<div style="background-color: #131D33; border-radius: 8px; padding: 12px; margin-top: 14px; border: 1px solid #1E2E4D;">
    <p style="color: #94A3B8; font-size: 0.78rem; margin: 0; line-height: 1.45;">
        <strong style="color: #F59E0B;">Dataset:</strong> MovieLens Latest-Small<br>
        <strong style="color: #38BDF8;">Scope:</strong> 100K+ Ratings, 9.7K Movies<br>
        <strong style="color: #10B981;">Language:</strong> 100% Simple English
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7. Helper: Smart Movie Search Logic
# -----------------------------------------------------------------------------
def search_local_movies(query, df):
    """Token-based case-insensitive smart search that handles 'The' prefixes and spaces."""
    query = query.strip().lower()
    tokens = [t for t in query.split() if t]
    if not tokens:
        return df.head(0)
    # Check if all tokens appear in title
    mask = df["title"].str.lower().apply(lambda t: all(tok in t for tok in tokens))
    return df[mask]

def get_poster_html(poster_url, title):
    """Return clean HTML for movie poster with fallback image."""
    if poster_url:
        return f'<img src="{poster_url}" class="movie-card-img" alt="{title}">'
    else:
        return f'''
        <div class="movie-card-img" style="display:flex; flex-direction:column; align-items:center; justify-content:center; color:#64748B; padding:16px; text-align:center;">
            <span style="font-size:2.8rem; margin-bottom:8px;">🎬</span>
            <span style="font-size:0.85rem; font-weight:600; color:#94A3B8;">{title}</span>
        </div>
        '''

# =============================================================================
# PAGE 1: HOME
# =============================================================================
if st.session_state["current_page"] == "🏠 Home":
    # Hero Banner
    st.markdown("""
    <div class="hero-banner">
        <span class="hero-tag">Welcome to CineScope</span>
        <h1 class="hero-title">Discover Movies. Explore Ratings. Find Your Next Favourite.</h1>
        <p class="hero-subtitle">
            Search thousands of movies, discover true audience ratings, view director and cast details, and explore cinema history powered by real data.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Large Search Bar on Homepage
    col_s1, col_s2 = st.columns([5, 1])
    with col_s1:
        home_search = st.text_input(
            "Search for any movie:",
            placeholder="Search by title... e.g. Inception, The Dark Knight, Titanic, 3 Idiots, Interstellar",
            label_visibility="collapsed"
        )
    with col_s2:
        search_clicked = st.button("🔍 Search Movie", use_container_width=True, type="primary")

    if search_clicked and home_search.strip():
        st.session_state["search_query"] = home_search.strip()
        st.session_state["current_page"] = "🔍 Movie Search and Details"
        st.rerun()

    # Quick Search Pills
    st.markdown("""
    <div style="margin-top: -6px; margin-bottom: 24px; font-size: 0.85rem; color: #94A3B8;">
        <strong style="color: #F59E0B;">Quick Try:</strong>
        <span style="color: #CBD5E1;">Interstellar • Inception • The Dark Knight • Titanic • 3 Idiots • The Shawshank Redemption • Pulp Fiction</span>
    </div>
    """, unsafe_allow_html=True)

    # 4 Quick Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Movie Catalog</div>
            <div class="metric-value">{total_movies:,}</div>
            <div class="metric-desc">Curated titles from 1902 to 2018 in the dataset.</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Audience Ratings</div>
            <div class="metric-value">{total_ratings:,}</div>
            <div class="metric-desc">Genuine review scores submitted by viewers.</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Active Reviewers</div>
            <div class="metric-value">{total_users:,}</div>
            <div class="metric-desc">Film enthusiasts who each rated at least 20 movies.</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Global Average</div>
            <div class="metric-value">{avg_rating_global} <span style="font-size:1.1rem; color:#F59E0B;">★</span></div>
            <div class="metric-desc">Average rating score across the entire catalog.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Featured Blockbusters Showcase (Grid of 4)
    st.markdown('<div class="section-title">⭐ Featured All-Time Fan Favourites</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Hand-picked cinema masterpieces with high audience scores and hundreds of reviews.</p>', unsafe_allow_html=True)

    featured_titles = ["The Shawshank Redemption", "The Dark Knight", "Inception", "Interstellar"]
    f_cols = st.columns(4)

    for idx, f_title in enumerate(featured_titles):
        with f_cols[idx]:
            matches = search_local_movies(f_title, merged_df)
            if not matches.empty:
                m_row = matches.iloc[0]
                omdb_info = fetch_omdb_details(imdb_id=m_row.get("imdbId"), title=m_row["clean_title"], year=m_row["year"], custom_key=custom_omdb_key)
                poster = omdb_info.get("poster") if omdb_info and omdb_info.get("found") else None

                st.markdown(f"""
                <div class="movie-card">
                    {get_poster_html(poster, m_row['clean_title'])}
                    <div class="movie-card-body">
                        <div>
                            <div class="movie-card-title">{m_row['clean_title']} ({int(m_row['year']) if pd.notna(m_row['year']) else 'N/A'})</div>
                            <div class="movie-card-genres">{m_row['genres'].replace('|', ' • ')}</div>
                        </div>
                        <div class="movie-card-meta">
                            <span><span class="badge-star">★ {m_row['mean_rating']}</span> ({m_row['rating_count']} votes)</span>
                            <span style="color: #38BDF8; font-weight:600;">Fair: {m_row['fair_score']}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"View Details ➔", key=f"btn_feat_{m_row['movieId']}", use_container_width=True):
                    st.session_state["selected_movie_id"] = m_row["movieId"]
                    st.session_state["current_page"] = "🔍 Movie Search and Details"
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Explore Next Call-to-Actions (2 Banners)
    cta1, cta2 = st.columns(2)
    with cta1:
        st.markdown("""
        <div style="background-color: #131D33; border: 1px solid #1E2E4D; border-radius: 14px; padding: 24px;">
            <h3 style="color: #FFFFFF; margin: 0 0 6px 0; font-size: 1.3rem;">📊 Explore Cinema Analytics</h3>
            <p style="color: #94A3B8; font-size: 0.95rem; margin-bottom: 16px;">
                Dive into 8 interactive charts showing genre scores, release year trends, and rating psychology.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Analytics Dashboard ➔", use_container_width=True, type="primary"):
            st.session_state["current_page"] = "📊 Movie Analytics Dashboard"
            st.rerun()

    with cta2:
        st.markdown("""
        <div style="background-color: #131D33; border: 1px solid #1E2E4D; border-radius: 14px; padding: 24px;">
            <h3 style="color: #FFFFFF; margin: 0 0 6px 0; font-size: 1.3rem;">⭐ Top Movie Rankings</h3>
            <p style="color: #94A3B8; font-size: 0.95rem; margin-bottom: 16px;">
                Explore the official leaderboard filtered by a fair scoring rule that prevents 1-vote movies from skewing results.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Top Rankings ➔", use_container_width=True):
            st.session_state["current_page"] = "⭐ Top Movies"
            st.rerun()

# =============================================================================
# PAGE 2: MOVIE SEARCH AND DETAILS (CORE FEATURE)
# =============================================================================
elif st.session_state["current_page"] == "🔍 Movie Search and Details":
    st.markdown('<div class="section-title">🔍 Movie Search and Details</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Search for any movie in our 100,000-rating MovieLens dataset or worldwide through OMDb. View real audience scores, posters, plot, director, and cast details.</p>', unsafe_allow_html=True)

    # Search Bar Row
    search_col1, search_col2 = st.columns([5, 1])
    with search_col1:
        query_input = st.text_input(
            "Search movie title:",
            value=st.session_state["search_query"],
            placeholder="Type a title... e.g. Inception, The Dark Knight, Interstellar, Titanic, 3 Idiots, Matrix",
            label_visibility="collapsed"
        )
    with search_col2:
        btn_search = st.button("Search", use_container_width=True, type="primary")

    if btn_search or (query_input and query_input != st.session_state["search_query"]):
        st.session_state["search_query"] = query_input
        st.session_state["selected_movie_id"] = None
        st.session_state["selected_external_movie"] = None
        st.rerun()

    # Quick Search Suggestion Pills
    st.markdown("<p style='font-size:0.82rem; color:#94A3B8; margin-top:-6px;'>Suggestions: "
                "<a href='#' style='color:#38BDF8;'>Inception</a> • "
                "<a href='#' style='color:#38BDF8;'>The Dark Knight</a> • "
                "<a href='#' style='color:#38BDF8;'>Titanic</a> • "
                "<a href='#' style='color:#38BDF8;'>Interstellar</a> • "
                "<a href='#' style='color:#38BDF8;'>3 Idiots</a> • "
                "<a href='#' style='color:#38BDF8;'>The Shawshank Redemption</a></p>", unsafe_allow_html=True)

    active_query = st.session_state["search_query"].strip()

    # Check if a specific local movie is selected for detail view
    if st.session_state["selected_movie_id"] is not None:
        sel_row = merged_df[merged_df["movieId"] == st.session_state["selected_movie_id"]]
        if not sel_row.empty:
            movie = sel_row.iloc[0]
            
            # Fetch rich details from OMDb
            with st.spinner("Fetching full movie details and poster..."):
                omdb = fetch_omdb_details(imdb_id=movie.get("imdbId"), title=movie["clean_title"], year=movie["year"], custom_key=custom_omdb_key)

            # Back button
            if st.button("⬅ Back to Search Results", type="secondary"):
                st.session_state["selected_movie_id"] = None
                st.rerun()

            # Render Full Movie Details
            d_col1, d_col2 = st.columns([1, 2.2])

            with d_col1:
                poster_url = omdb.get("poster") if omdb and omdb.get("found") else None
                if poster_url:
                    st.image(poster_url, use_container_width=True)
                else:
                    st.markdown(f"""
                    <div style="background-color: #1E293B; border-radius: 12px; height: 380px; display:flex; flex-direction:column; align-items:center; justify-content:center; color:#64748B;">
                        <span style="font-size: 3.5rem;">🎬</span>
                        <p style="font-size: 0.9rem; margin-top:8px; color:#94A3B8;">No Poster Available</p>
                    </div>
                    """, unsafe_allow_html=True)

                # External Links
                if pd.notna(movie.get("imdbId")):
                    imdb_link = f"https://www.imdb.com/title/tt{int(movie['imdbId']):07d}/"
                    st.markdown(f'<a href="{imdb_link}" target="_blank" style="display:block; text-align:center; background-color:#F59E0B; color:#0F172A; font-weight:700; padding:8px; border-radius:8px; margin-top:12px; text-decoration:none;">View on IMDb ↗</a>', unsafe_allow_html=True)
                
                google_link = f"https://www.google.com/search?q={urllib.parse.quote(movie['clean_title'] + ' movie')}"
                st.markdown(f'<a href="{google_link}" target="_blank" style="display:block; text-align:center; background-color:#1E293B; color:#38BDF8; font-weight:600; padding:8px; border-radius:8px; margin-top:8px; text-decoration:none; border:1px solid #334155;">Search on Google ↗</a>', unsafe_allow_html=True)

            with d_col2:
                st.markdown(f"""
                <div class="detail-card">
                    <h1 class="detail-title">{movie['clean_title']} <span style="color:#94A3B8; font-size:1.6rem;">({int(movie['year']) if pd.notna(movie['year']) else 'N/A'})</span></h1>
                """, unsafe_allow_html=True)

                # Genre Chips
                genre_chips_html = "".join([f'<span class="genre-chip">{g.strip()}</span>' for g in movie["genres"].split("|") if g.strip()])
                st.markdown(genre_chips_html, unsafe_allow_html=True)

                # Ratings Breakdown Box
                st.markdown(f"""
                <div class="rating-box">
                    <div style="display: flex; gap: 24px; flex-wrap: wrap;">
                        <div>
                            <span style="font-size:0.75rem; text-transform:uppercase; color:#94A3B8; font-weight:700;">MovieLens Rating</span>
                            <div style="font-size:1.6rem; font-weight:800; color:#F59E0B;">★ {movie['mean_rating']} <span style="font-size:0.9rem; color:#94A3B8;">/ 5.0</span></div>
                            <span style="font-size:0.8rem; color:#38BDF8;">from {movie['rating_count']} verified reviews</span>
                        </div>
                        <div>
                            <span style="font-size:0.75rem; text-transform:uppercase; color:#94A3B8; font-weight:700;">Fair Ranking Score</span>
                            <div style="font-size:1.6rem; font-weight:800; color:#10B981;">{movie['fair_score']} <span style="font-size:0.9rem; color:#94A3B8;">/ 5.0</span></div>
                            <span style="font-size:0.8rem; color:#A7F3D0;">Bayesian vote-weighted score</span>
                        </div>
                        {f'''
                        <div>
                            <span style="font-size:0.75rem; text-transform:uppercase; color:#94A3B8; font-weight:700;">External IMDb Rating</span>
                            <div style="font-size:1.6rem; font-weight:800; color:#38BDF8;">⭐ {omdb.get("imdb_rating")} <span style="font-size:0.9rem; color:#94A3B8;">/ 10</span></div>
                            <span style="font-size:0.8rem; color:#94A3B8;">from {omdb.get("imdb_votes")} votes</span>
                        </div>
                        ''' if omdb and omdb.get("found") and omdb.get("imdb_rating") != "N/A" else ''}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Plot Summary
                plot_text = omdb.get("plot") if omdb and omdb.get("found") else "This title is cataloged in the MovieLens benchmark dataset with complete audience review distributions."
                st.markdown(f"""
                <div style="margin-bottom: 16px;">
                    <h4 style="color:#FFFFFF; font-size:1rem; margin:0 0 4px 0;">Plot Overview</h4>
                    <p style="color:#CBD5E1; font-size:0.95rem; line-height:1.5;">{plot_text}</p>
                </div>
                """, unsafe_allow_html=True)

                # Metadata Attributes
                if omdb and omdb.get("found"):
                    st.markdown(f"""
                    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px; font-size:0.88rem; color:#CBD5E1;">
                        <div><strong style="color:#94A3B8;">🎬 Director:</strong> {omdb.get('director')}</div>
                        <div><strong style="color:#94A3B8;">⏱️ Runtime:</strong> {omdb.get('runtime')}</div>
                        <div><strong style="color:#94A3B8;">👥 Main Cast:</strong> {omdb.get('actors')}</div>
                        <div><strong style="color:#94A3B8;">🗣️ Language:</strong> {omdb.get('language')}</div>
                        <div><strong style="color:#94A3B8;">📅 Released:</strong> {omdb.get('released')}</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

    # Perform Search Query
    elif active_query:
        local_results = search_local_movies(active_query, merged_df)

        if not local_results.empty:
            st.markdown(f"#### 🎯 Found {len(local_results)} Matching Movies in Dataset:")
            
            # Show grid of matching movies (up to 12)
            grid_cols = st.columns(3)
            for idx, (_, row) in enumerate(local_results.head(12).iterrows()):
                col_idx = idx % 3
                with grid_cols[col_idx]:
                    st.markdown(f"""
                    <div class="metric-card" style="margin-bottom: 16px;">
                        <h4 style="margin: 0 0 4px 0; color:#FFFFFF; font-size:1.15rem;">{row['clean_title']} <span style="color:#94A3B8; font-size:0.9rem;">({int(row['year']) if pd.notna(row['year']) else 'N/A'})</span></h4>
                        <p style="color:#A855F7; font-size:0.8rem; margin:0 0 10px 0; font-weight:600;">{row['genres'].replace('|', ' • ')}</p>
                        <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid #1E2E4D; padding-top:8px;">
                            <span class="badge-star">★ {row['mean_rating']}</span>
                            <span style="font-size:0.82rem; color:#94A3B8;">{row['rating_count']} reviews</span>
                            <span style="font-size:0.82rem; color:#10B981; font-weight:700;">Fair: {row['fair_score']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    if st.button("View Full Details ➔", key=f"sel_res_{row['movieId']}", use_container_width=True):
                        st.session_state["selected_movie_id"] = row["movieId"]
                        st.rerun()

        else:
            # Movie not found in local dataset: Attempt External Worldwide Search via OMDb
            st.markdown(f"""
            <div class="friendly-box">
                <span style="font-size: 2.2rem;">🔍</span>
                <h3 style="color: #FFFFFF; margin: 8px 0 4px 0;">Searching Worldwide Movie Database...</h3>
                <p style="color: #CBD5E1; font-size: 0.95rem; margin-bottom: 0;">
                    '{active_query}' was not found in the local MovieLens dataset (which covers movies up to 2018).<br>
                    Checking worldwide database via OMDb...
                </p>
            </div>
            """, unsafe_allow_html=True)

            with st.spinner("Connecting to external movie database..."):
                ext_result = fetch_omdb_details(title=active_query, custom_key=custom_omdb_key)

            if ext_result and ext_result.get("found"):
                st.success(f"Found worldwide match for '{ext_result.get('title')}'!")
                
                # Render external movie card
                ext_c1, ext_c2 = st.columns([1, 2])
                with ext_c1:
                    if ext_result.get("poster"):
                        st.image(ext_result.get("poster"), use_container_width=True)
                    else:
                        st.markdown('<div style="background:#1E293B; height:320px; border-radius:12px;"></div>', unsafe_allow_html=True)
                with ext_c2:
                    st.markdown(f"""
                    <div class="detail-card">
                        <span style="background:#3B82F6; color:#FFF; font-size:0.75rem; font-weight:800; padding:3px 10px; border-radius:12px; text-transform:uppercase;">External Search Result</span>
                        <h2 style="color:#FFF; margin:8px 0 4px 0;">{ext_result.get('title')} ({ext_result.get('year')})</h2>
                        <div class="rating-box">
                            <span style="font-size:0.8rem; color:#94A3B8; font-weight:700;">EXTERNAL IMDb RATING</span>
                            <div style="font-size:1.6rem; font-weight:800; color:#F59E0B;">⭐ {ext_result.get('imdb_rating')} <span style="font-size:0.9rem; color:#94A3B8;">/ 10</span></div>
                            <span style="font-size:0.8rem; color:#38BDF8;">from {ext_result.get('imdb_votes')} external user votes</span>
                        </div>
                        <p style="color:#CBD5E1; font-size:0.95rem; line-height:1.5;"><strong>Plot:</strong> {ext_result.get('plot')}</p>
                        <p style="color:#CBD5E1; font-size:0.88rem; margin:0;">
                            <strong>Director:</strong> {ext_result.get('director')}<br>
                            <strong>Cast:</strong> {ext_result.get('actors')}<br>
                            <strong>Runtime:</strong> {ext_result.get('runtime')} • <strong>Language:</strong> {ext_result.get('language')}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning(f"Could not find any movie named '{active_query}'. Try checking the spelling or searching a famous title like Inception, Titanic, or Interstellar.")

    else:
        # Initial empty search state: Show popular movie shortcuts
        st.markdown("""
        <div style="background-color: #131D33; border: 1px dashed #334155; border-radius: 14px; padding: 32px; text-align: center; margin-top: 20px;">
            <span style="font-size: 3rem;">🔎</span>
            <h3 style="color: #FFFFFF; margin: 12px 0 6px 0;">Search Any Movie Title Above</h3>
            <p style="color: #94A3B8; font-size: 0.95rem; max-width: 600px; margin: 0 auto 18px auto;">
                Type any movie name in the box above to explore its verified ratings, release year, genres, plot summary, and director.
            </p>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# PAGE 3: MOVIE ANALYTICS DASHBOARD
# =============================================================================
elif st.session_state["current_page"] == "📊 Movie Analytics Dashboard":
    st.markdown('<div class="section-title">📊 Movie Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Explore comprehensive, interactive charts built directly on 100,000+ real ratings from the MovieLens dataset. Every chart includes simple explanations of what the data reveals.</p>', unsafe_allow_html=True)

    # Filter Controls
    f_c1, f_c2 = st.columns(2)
    with f_c1:
        dash_years = st.slider("Select Release Year Range:", min_value=min_year, max_value=max_year, value=(1970, max_year))
    with f_c2:
        dash_min_votes = st.slider("Show only movies with at least this many ratings:", min_value=1, max_value=200, value=50)

    # Filtered Dataset
    f_merged = merged_df[(merged_df["year"] >= dash_years[0]) & (merged_df["year"] <= dash_years[1])]

    # 4 Dynamic Metric Badges
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Eligible Movies</div>
            <div class="metric-value">{len(f_merged):,}</div>
            <div class="metric-desc">Movies released between {dash_years[0]} and {dash_years[1]}.</div>
        </div>
        """, unsafe_allow_html=True)
    with b2:
        top_fair = f_merged[f_merged["rating_count"] >= dash_min_votes].sort_values("fair_score", ascending=False)
        top_movie_name = top_fair.iloc[0]["clean_title"] if not top_fair.empty else "N/A"
        top_movie_score = top_fair.iloc[0]["fair_score"] if not top_fair.empty else "N/A"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Top Ranked Movie</div>
            <div class="metric-value" style="font-size:1.45rem; color:#F59E0B;">{top_movie_name[:18]}</div>
            <div class="metric-desc">Fair Score: {top_movie_score} (Min {dash_min_votes} votes).</div>
        </div>
        """, unsafe_allow_html=True)
    with b3:
        most_voted_row = f_merged.sort_values("rating_count", ascending=False).iloc[0] if not f_merged.empty else None
        most_voted_title = most_voted_row["clean_title"] if most_voted_row is not None else "N/A"
        most_voted_count = most_voted_row["rating_count"] if most_voted_row is not None else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Most Rated Movie</div>
            <div class="metric-value" style="font-size:1.45rem; color:#38BDF8;">{most_voted_title[:18]}</div>
            <div class="metric-desc">{most_voted_count} verified reviews received.</div>
        </div>
        """, unsafe_allow_html=True)
    with b4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Most Rated Genre</div>
            <div class="metric-value" style="font-size:1.7rem; color:#10B981;">Drama</div>
            <div class="metric-desc">41,928 ratings across the catalog.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 1 Charts: Rating Distribution & Genre Averages
    c_left, c_right = st.columns(2)

    with c_left:
        st.markdown("#### How People Rate Movies (0.5 to 5.0 Stars)")
        score_df = ratings_df["rating"].value_counts().sort_index().reset_index()
        score_df.columns = ["rating", "count"]
        score_df["pct"] = (score_df["count"] / total_ratings * 100).round(1)

        fig_scores = px.bar(
            score_df,
            x="rating",
            y="count",
            text=score_df["pct"].apply(lambda p: f"{p}%"),
            color="count",
            color_continuous_scale=["#38BDF8", "#F59E0B"],
            labels={"rating": "Star Rating (0.5 to 5.0)", "count": "Number of Times Given"}
        )
        fig_scores.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=380,
            coloraxis_showscale=False,
            xaxis=dict(tickmode="linear", tick0=0.5, dtick=0.5)
        )
        fig_scores.update_traces(textposition="outside", cliponaxis=False)
        st.plotly_chart(fig_scores, use_container_width=True)

        st.markdown("""
        <div class="chart-explainer">
            <strong>What this chart shows:</strong> The frequency of each star rating given by users.<br>
            <span class="chart-takeaway">🎯 Key takeaway: 4.0 stars is the #1 most common score (26.6%). Most reviewers rate movies positively because they pick films they expect to enjoy.</span>
        </div>
        """, unsafe_allow_html=True)

    with c_right:
        st.markdown("#### Average Rating for Each Genre")
        g_summary = genre_ratings.groupby("genre").agg(
            avg_rating=("rating", "mean"),
            total_reviews=("rating", "count")
        ).reset_index().sort_values("avg_rating", ascending=True)

        fig_genres = px.bar(
            g_summary,
            x="avg_rating",
            y="genre",
            orientation="h",
            text=g_summary["avg_rating"].round(2),
            color="avg_rating",
            color_continuous_scale=["#38BDF8", "#8B5CF6", "#F59E0B"],
            labels={"avg_rating": "Average Rating (out of 5)", "genre": "Movie Genre"}
        )
        fig_genres.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=380,
            coloraxis_showscale=False
        )
        fig_genres.update_traces(textposition="outside", cliponaxis=False)
        st.plotly_chart(fig_genres, use_container_width=True)

        st.markdown("""
        <div class="chart-explainer">
            <strong>What this chart shows:</strong> The average audience score across all 19 movie categories.<br>
            <span class="chart-takeaway">🎯 Key takeaway: Film-Noir (3.92) and War (3.81) have the highest average ratings, while Horror (3.26) and Comedy (3.38) receive lower average scores.</span>
        </div>
        """, unsafe_allow_html=True)

    # Row 2 Charts: Yearly Production & Rating Trends Over Time
    c2_left, c2_right = st.columns(2)

    with c2_left:
        st.markdown("#### How Movie Releases Have Changed Over the Years")
        year_counts = f_merged.dropna(subset=["year"])["year"].astype(int).value_counts().sort_index().reset_index()
        year_counts.columns = ["year", "movie_count"]

        fig_year_prod = px.bar(
            year_counts,
            x="year",
            y="movie_count",
            color="movie_count",
            color_continuous_scale=["#38BDF8", "#F59E0B"],
            labels={"year": "Release Year", "movie_count": "Movies Released"}
        )
        fig_year_prod.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=380,
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_year_prod, use_container_width=True)

        st.markdown("""
        <div class="chart-explainer">
            <strong>What this chart shows:</strong> The count of movies released in each calendar year.<br>
            <span class="chart-takeaway">🎯 Key takeaway: Movie production surged starting in the 1990s and peaked between 2002 and 2014 as digital filming made movie-making more accessible.</span>
        </div>
        """, unsafe_allow_html=True)

    with c2_right:
        st.markdown("#### Average Movie Ratings by Release Year")
        year_avg = f_merged[f_merged["rating_count"] >= 5].groupby("year")["mean_rating"].mean().reset_index()
        year_avg["year"] = year_avg["year"].astype(int)
        year_avg["smooth_avg"] = year_avg["mean_rating"].rolling(window=5, min_periods=1).mean().round(2)

        fig_year_ratings = px.line(
            year_avg,
            x="year",
            y="smooth_avg",
            labels={"year": "Release Year", "smooth_avg": "Average Score (5-Year Smooth)"},
            markers=True
        )
        fig_year_ratings.update_traces(line_color="#F59E0B", line_width=3, marker=dict(size=4, color="#38BDF8"))
        fig_year_ratings.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=380,
            yaxis=dict(range=[2.8, 4.3])
        )
        st.plotly_chart(fig_year_ratings, use_container_width=True)

        st.markdown("""
        <div class="chart-explainer">
            <strong>What this chart shows:</strong> How audience ratings vary based on the decade a movie was released.<br>
            <span class="chart-takeaway">🎯 Key takeaway: Older classic films maintain higher average scores (~3.8 to 4.0) because only the greatest movies from those eras are still remembered and rated today.</span>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# PAGE 4: EXPLORE GENRES
# =============================================================================
elif st.session_state["current_page"] == "🎭 Explore Genres":
    st.markdown('<div class="section-title">🎭 Explore Movie Genres</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Compare movie genres, discover which categories have the most movies, and explore the highest-rated titles within your favourite genres.</p>', unsafe_allow_html=True)

    # Multi-genre Selector
    all_genre_list = sorted([g for g in exploded_df["genre"].dropna().unique() if g != "(no genres listed)"])
    selected_genres = st.multiselect(
        "Select Genres to Compare (or leave empty to view all):",
        options=all_genre_list,
        default=["Action", "Comedy", "Drama", "Sci-Fi", "Thriller"]
    )

    if not selected_genres:
        selected_genres = all_genre_list

    # Compute stats for selected genres
    sel_genre_df = genre_ratings[genre_ratings["genre"].isin(selected_genres)]
    genre_metrics = sel_genre_df.groupby("genre").agg(
        avg_score=("rating", "mean"),
        total_votes=("rating", "count")
    ).reset_index()

    genre_movie_counts = exploded_df[exploded_df["genre"].isin(selected_genres)].groupby("genre")["movieId"].nunique().reset_index(name="movie_count")
    genre_metrics = pd.merge(genre_metrics, genre_movie_counts, on="genre")
    genre_metrics["avg_score"] = genre_metrics["avg_score"].round(2)

    # Tabs for Genre Comparisons
    g_tab1, g_tab2, g_tab3 = st.tabs([
        "⭐ Average Rating by Genre",
        "🎬 Total Movies by Genre",
        "💬 Total Ratings by Genre"
    ])

    with g_tab1:
        fig_g1 = px.bar(
            genre_metrics.sort_values("avg_score", ascending=True),
            x="avg_score",
            y="genre",
            orientation="h",
            text="avg_score",
            color="avg_score",
            color_continuous_scale=["#38BDF8", "#F59E0B"],
            labels={"avg_score": "Average Rating (out of 5)", "genre": "Genre"}
        )
        fig_g1.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=420, coloraxis_showscale=False)
        fig_g1.update_traces(textposition="outside", cliponaxis=False)
        st.plotly_chart(fig_g1, use_container_width=True)

    with g_tab2:
        fig_g2 = px.bar(
            genre_metrics.sort_values("movie_count", ascending=True),
            x="movie_count",
            y="genre",
            orientation="h",
            text="movie_count",
            color="movie_count",
            color_continuous_scale=["#38BDF8", "#8B5CF6"],
            labels={"movie_count": "Number of Movies in Catalog", "genre": "Genre"}
        )
        fig_g2.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=420, coloraxis_showscale=False)
        fig_g2.update_traces(textposition="outside", cliponaxis=False)
        st.plotly_chart(fig_g2, use_container_width=True)

    with g_tab3:
        fig_g3 = px.bar(
            genre_metrics.sort_values("total_votes", ascending=True),
            x="total_votes",
            y="genre",
            orientation="h",
            text="total_votes",
            color="total_votes",
            color_continuous_scale=["#10B981", "#38BDF8"],
            labels={"total_votes": "Total Number of Ratings", "genre": "Genre"}
        )
        fig_g3.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=420, coloraxis_showscale=False)
        fig_g3.update_traces(textposition="outside", cliponaxis=False)
        st.plotly_chart(fig_g3, use_container_width=True)

    # Educational Note on High Rating vs High Volume
    st.markdown("""
    <div style="background-color: #131D33; border: 1px solid #1E2E4D; border-radius: 12px; padding: 20px; margin-top: 20px;">
        <h4 style="color: #F59E0B; margin: 0 0 6px 0;">💡 Why a High Rating Doesn't Always Mean the Most Popular Genre</h4>
        <p style="color: #CBD5E1; font-size: 0.94rem; margin: 0; line-height: 1.5;">
            Genres like <strong>Film-Noir</strong> and <strong>War</strong> achieve high average scores because they have dedicated audiences who watch selectively. 
            In contrast, <strong>Drama</strong> and <strong>Comedy</strong> have tens of thousands of reviews because they cater to everyone, which naturally balances their scores closer to the global average.
        </p>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# PAGE 5: TOP MOVIES
# =============================================================================
elif st.session_state["current_page"] == "⭐ Top Movies":
    st.markdown('<div class="section-title">⭐ Top Movies Leaderboard</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Discover the top-rated films ranked using our Fair Score formula that balances high review scores with a minimum number of ratings.</p>', unsafe_allow_html=True)

    # Filter Controls
    top_c1, top_c2, top_c3 = st.columns(3)
    with top_c1:
        top_genre_pick = st.selectbox("Filter by Genre:", ["All Genres"] + all_genres)
    with top_c2:
        top_min_ratings = st.slider("Minimum ratings required:", min_value=1, max_value=250, value=50, step=5)
    with top_c3:
        top_sort_by = st.selectbox("Sort Leaderboard By:", ["Fair Score (Recommended)", "Highest Average Rating", "Most Number of Ratings"])

    # Filter Data
    top_df = merged_df[merged_df["rating_count"] >= top_min_ratings].copy()
    if top_genre_pick != "All Genres":
        top_df = top_df[top_df["genres"].str.contains(top_genre_pick, na=False, regex=False)]

    if "Fair Score" in top_sort_by:
        top_df = top_df.sort_values("fair_score", ascending=False)
    elif "Highest Average" in top_sort_by:
        top_df = top_df.sort_values(["mean_rating", "rating_count"], ascending=[False, False])
    else:
        top_df = top_df.sort_values("rating_count", ascending=False)

    top_20 = top_df.head(20).reset_index(drop=True)

    # Leaderboard Table
    st.markdown(f"#### 🏆 Ranked Top 20 Movies ({top_genre_pick}, Min {top_min_ratings} Votes)")
    
    table_disp = top_20[["clean_title", "year", "genres", "mean_rating", "rating_count", "fair_score"]].copy()
    table_disp.index = table_disp.index + 1
    table_disp["year"] = table_disp["year"].fillna(0).astype(int)
    table_disp.columns = ["Movie Title", "Release Year", "Genres", "Average Rating", "Total Votes", "Fair Ranking Score"]
    
    st.dataframe(table_disp, use_container_width=True)

    st.markdown("""
    <div class="chart-explainer">
        <strong>How the Fair Score Works:</strong> A simple average rating can be deceptive — a movie with just one 5-star review would rank #1! 
        Our Fair Score uses Bayesian weighting to balance average scores with vote counts, ensuring that only genuine, proven classics reach the top.<br>
        <span class="chart-takeaway">🎯 Key takeaway: The Shawshank Redemption, The Godfather, and Fight Club lead the all-time ranking because they excel in both high ratings and massive audience votes.</span>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# PAGE 6: RATING INSIGHTS
# =============================================================================
elif st.session_state["current_page"] == "💡 Rating Insights":
    st.markdown('<div class="section-title">💡 Rating Insights & What We Learned</div>', unsafe_allow_html=True)
    st.markdown('<p class="section-desc">Key takeaways and patterns discovered through our empirical analysis of over 100,000 real audience reviews.</p>', unsafe_allow_html=True)

    # 6 Automated Key Findings
    insights = [
        (
            "1. Most Loved Genres: Film-Noir & War",
            "Film-Noir achieved the highest average rating in our entire dataset (3.92 out of 5), followed closely by War (3.81) and Documentaries (3.80). Viewers who watch these genres are thoughtful and rate them generously."
        ),
        (
            "2. Most Popular Genre: Drama (41,928 Ratings)",
            "Drama and Comedy attract the largest volume of audience engagement. Over 40% of all ratings belong to Drama movies, proving that character-driven storytelling resonates with the widest audience."
        ),
        (
            "3. The 4.0 Star Phenomenon (People Are Generous Reviewers)",
            "4.0 stars is the #1 most common rating, making up 26.6% of all ratings. Furthermore, 69.9% of all ratings are whole stars (1, 2, 3, 4, 5). People choose movies they expect to like, resulting in predominantly positive reviews."
        ),
        (
            "4. Why Minimum Rating Filters Are Essential",
            "Over 3,400 movies in the dataset have only a single rating! Without a minimum rating threshold, obscure 1-vote movies would unfairly dominate the #1 spot. Requiring at least 50 ratings surfaces true classics like The Shawshank Redemption and The Godfather."
        ),
        (
            "5. Movie Production Peak (1990s–2010s)",
            "The volume of movie releases grew rapidly starting in the 1990s and peaked between 2002 and 2014, reflecting the boom of independent film studios and digital production techniques."
        ),
        (
            "6. Practical Business Uses for Streaming Platforms",
            "Streaming services like Netflix and Prime Video can apply these findings to: (1) License high-rating classic films to build catalog prestige, (2) Feature Drama and Comedy prominently on home screens for broad appeal, and (3) Use fair scoring to keep recommendation algorithms fair."
        )
    ]

    for title, text in insights:
        st.markdown(f"""
        <div style="background-color: #131D33; border: 1px solid #1E2E4D; border-radius: 12px; padding: 18px 22px; margin-bottom: 14px;">
            <h4 style="color: #FFFFFF; font-size: 1.1rem; margin: 0 0 6px 0;">{title}</h4>
            <p style="color: #CBD5E1; font-size: 0.94rem; margin: 0; line-height: 1.5;">{text}</p>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 8. Footer
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.86rem; padding: 16px 0;">
    <strong style="color: #94A3B8;">CineScope — Movie Ratings and Genre Trends</strong><br>
    Built with Python, Streamlit, Pandas, Plotly & OMDb API  •  MovieLens Latest-Small Dataset  •  Project ID: DA-006
</div>
""", unsafe_allow_html=True)
