"""Movie search page for Streamlit Hello App."""

import streamlit as st
from typing import Dict, List, Any, Optional
import logging

from streamlit_hello_app.utils import get_tmdb_api_key, validate_tmdb_api_key, TMDB_API_KEY_VALID
from streamlit_hello_app.modules.tmdb_service import TmdbService


def render_movie_search() -> None:
    """Render the movie search page."""
    st.header("🎬 Movie Search")
    st.markdown("Search for movies using The Movie Database (TMDB)")
    
    # Get API key
    api_key = get_tmdb_api_key()
    
    if not api_key:
        st.error("❌ No TMDB API key found. Please set TMDB_API_KEY environment variable or enter your API key.")
        st.info("Get your API key from [TMDB Settings](https://www.themoviedb.org/settings/api)")
        return
    
    # Validate API key
    validation_result = validate_tmdb_api_key(api_key)
    
    if validation_result != TMDB_API_KEY_VALID:
        if validation_result == "invalid":
            st.error("❌ Invalid TMDB API key. Please check your key and try again.")
        else:
            st.error("❌ Error validating TMDB API key. Please check your connection and try again.")
        st.info("Get your API key from [TMDB Settings](https://www.themoviedb.org/settings/api)")
        return
    
    # Search form
    with st.form("movie_search_form"):
        st.subheader("🔍 Search Movies")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_query = st.text_input(
                "Enter movie title:",
                placeholder="e.g., Inception, The Dark Knight, Avatar",
                help="Enter the name of the movie you want to search for"
            )
        
        with col2:
            search_button = st.form_submit_button("Search", type="primary")
    
    # Handle search
    if search_button and search_query:
        with st.spinner("Searching for movies..."):
            try:
                service = TmdbService(api_key)
                results = service.search_movies(search_query)
                
                if results['success']:
                    display_movie_results(results)
                else:
                    st.error(f"❌ Search failed: {results['error']}")
                    
            except Exception as e:
                logging.error(f"Movie search error: {e}")
                st.error(f"❌ An unexpected error occurred: {str(e)}")
    
    # Show help section
    st.markdown("---")
    with st.expander("ℹ️ How to use Movie Search"):
        st.markdown("""
        **Getting Started:**
        1. Get your free API key from [TMDB](https://www.themoviedb.org/settings/api)
        2. Set the `TMDB_API_KEY` environment variable or enter it when prompted
        3. Search for movies by entering the title in the search box
        4. Browse results with movie posters, ratings, and descriptions
        
        **Features:**
        - Search by movie title
        - View movie posters and details
        - See ratings and release years
        - Pagination support for large result sets
        
        **Tips:**
        - Use specific movie titles for better results
        - Try different spellings if you don't find your movie
        - Check the release year to find the right version
        """)


def display_movie_results(results: Dict[str, Any]) -> None:
    """
    Display movie search results.
    
    Args:
        results: Search results dictionary
    """
    movies = results.get('movies', [])
    total_results = results.get('total_results', 0)
    current_page = results.get('current_page', 1)
    total_pages = results.get('total_pages', 1)
    
    if not movies:
        st.info("🔍 No movies found. Try a different search term.")
        return
    
    # Results header
    st.success(f"✅ Found {total_results} movie(s)")
    
    # Display movies in grid
    if len(movies) == 1:
        # Single movie - display full width
        display_movie_card(movies[0], full_width=True)
    else:
        # Multiple movies - display in grid
        cols = st.columns(2)
        for i, movie in enumerate(movies):
            col_index = i % 2
            with cols[col_index]:
                display_movie_card(movie)
    
    # Pagination
    if total_pages > 1:
        st.markdown("---")
        st.subheader("📄 Pagination")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("⬅️ Previous", disabled=(current_page <= 1)):
                st.session_state.movie_search_page = current_page - 1
                st.rerun()
        
        with col2:
            st.write(f"Page {current_page} of {total_pages}")
        
        with col3:
            if st.button("Next ➡️", disabled=(current_page >= total_pages)):
                st.session_state.movie_search_page = current_page + 1
                st.rerun()
        
        with col4:
            if st.button("First ⏮️", disabled=(current_page <= 1)):
                st.session_state.movie_search_page = 1
                st.rerun()
        
        with col5:
            if st.button("Last ⏭️", disabled=(current_page >= total_pages)):
                st.session_state.movie_search_page = total_pages
                st.rerun()


def display_movie_card(movie: Dict[str, Any], full_width: bool = False) -> None:
    """
    Display a single movie card.
    
    Args:
        movie: Movie data dictionary
        full_width: Whether to display full width
    """
    with st.container():
        # Movie poster and info layout
        if full_width:
            col1, col2 = st.columns([1, 2])
        else:
            col1, col2 = st.columns([1, 2])
        
        with col1:
            # Movie poster
            if movie.get('poster_url'):
                st.image(
                    movie['poster_url'],
                    width=200,
                    caption=movie['title']
                )
            else:
                st.image(
                    "https://via.placeholder.com/200x300/404040/FFFFFF?text=No+Poster",
                    width=200,
                    caption="No poster available"
                )
        
        with col2:
            # Movie details
            st.markdown(f"### {movie['title']}")
            
            # Release year and rating
            col_year, col_rating = st.columns(2)
            with col_year:
                st.metric("Release Year", movie.get('release_year', 'Unknown'))
            with col_rating:
                rating = movie.get('vote_average', 0)
                vote_count = movie.get('vote_count', 0)
                st.metric(
                    "Rating", 
                    f"{rating:.1f}/10",
                    help=f"Based on {vote_count:,} votes"
                )
            
            # Overview
            st.markdown("**Overview:**")
            st.write(movie.get('overview', 'No overview available'))
            
            # Additional info
            if movie.get('vote_count', 0) > 0:
                st.caption(f"TMDB ID: {movie.get('id', 'N/A')}")
        
        st.markdown("---")


def format_movie_data(raw_movie: Dict[str, Any], poster_url: Optional[str] = None) -> Dict[str, Any]:
    """
    Format raw movie data for display.
    
    Args:
        raw_movie: Raw movie data from API
        poster_url: Optional poster URL
        
    Returns:
        Formatted movie data
    """
    # Extract release year
    release_date = raw_movie.get('release_date', '')
    release_year = 'Unknown'
    if release_date:
        try:
            release_year = release_date.split('-')[0]
        except (IndexError, AttributeError):
            release_year = 'Unknown'
    
    # Format overview
    overview = raw_movie.get('overview', '')
    if not overview:
        overview = 'No overview available'
    elif len(overview) > 200:
        overview = overview[:197] + '...'
    
    # Handle None values for numeric fields
    vote_average = raw_movie.get('vote_average')
    if vote_average is None:
        vote_average = 0.0
    
    vote_count = raw_movie.get('vote_count')
    if vote_count is None:
        vote_count = 0
    
    return {
        'id': raw_movie.get('id'),
        'title': raw_movie.get('title', 'Unknown Title'),
        'overview': overview,
        'poster_url': poster_url,
        'release_year': release_year,
        'vote_average': vote_average,
        'vote_count': vote_count
    }
