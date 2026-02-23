import sqlite3
import pandas as pd
from fuzzywuzzy import fuzz, process
import os
from pathlib import Path
def connect_to_playnite_db():
    """
    Connect to Playnite database.
    Common locations for Playnite database:
    - %APPDATA%/Playnite/library.db (Windows)
    - Or wherever you've installed Playnite
    """
    # Common Playnite database paths
    possible_paths = [
        os.path.expandvars(r"%APPDATA%\Playnite\library.db"),
        os.path.expandvars(r"%LOCALAPPDATA%\Playnite\library.db"),
        r"C:\Program Files\Playnite\library.db",
        r"C:\Program Files (x86)\Playnite\library.db",
    ]
    
    db_path = None
    for path in possible_paths:
        if os.path.exists(path):
            db_path = path
            break
    
    if not db_path:
        raise FileNotFoundError("Could not find Playnite database. Please provide the path manually.")
    
    return db_path

def get_playnite_games(db_path):
    """
    Extract game names from Playnite database.
    """
    try:
        conn = sqlite3.connect(db_path)
        # Query to get game names - adjust table/column names if needed
        query = "SELECT Name FROM Games WHERE Hidden = 0 OR Hidden IS NULL"
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        # Clean up names and remove duplicates
        games = df['Name'].dropna().unique().tolist()
        return games
    except Exception as e:
        print(f"Error reading Playnite database: {e}")
        return []

def load_games_to_match(file_path):
    """
    Load games from a file (CSV or text file).
    For CSV, assumes first column contains game names.
    For text, assumes one game per line.
    """
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
        # Assume first column contains game names
        games = df.iloc[:, 0].dropna().tolist()
    else:
        # Assume text file with one game per line
        with open(file_path, 'r', encoding='utf-8') as f:
            games = [line.strip() for line in f if line.strip()]
    
    return games

def fuzzy_match_games(source_games, target_games, threshold=80, limit=3):
    """
    Fuzzy match source games against target games.
    
    Args:
        source_games: List of games to find matches for
        target_games: List of games to match against (your Playnite collection)
        threshold: Minimum similarity score (0-100)
        limit: Number of top matches to return
    
    Returns:
        DataFrame with matches
    """
    results = []
    
    for source_game in source_games:
        # Get top matches
        matches = process.extract(source_game, target_games, scorer=fuzz.token_sort_ratio, limit=limit)
        
        # Filter by threshold
        good_matches = [(match, score) for match, score in matches if score >= threshold]
        
        if good_matches:
            for match, score in good_matches:
                results.append({
                    'Source_Game': source_game,
                    'Matched_Game': match,
                    'Score': score,
                    'Is_Top_Match': score == good_matches[0][1]  # Flag the best match
                })
        else:
            # No matches found above threshold
            results.append({
                'Source_Game': source_game,
                'Matched_Game': 'NO MATCH FOUND',
                'Score': 0,
                'Is_Top_Match': False
            })
    
    return pd.DataFrame(results)

def match_single_game(game_name, playnite_games=None, threshold=70):
    """
    Helper function to match a single game name.
    Useful for testing or interactive use.
    """
    if playnite_games is None:
        db_path = connect_to_playnite_db()
        playnite_games = get_playnite_games(db_path)
    
    matches = process.extract(game_name, playnite_games, scorer=fuzz.token_sort_ratio, limit=5)
    good_matches = [(match, score) for match, score in matches if score >= threshold]
    
    return good_matches