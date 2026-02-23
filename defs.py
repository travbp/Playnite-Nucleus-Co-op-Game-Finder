import pandas as pd
from fuzzywuzzy import fuzz, process
import os

def get_playnite_games(playnite_games_file_path="~/games.txt"):
    """
    Load Playnite game names from file
    """
    # Expand ~ to the full user home path (cross-platform)
    playnite_games_file_path = os.path.expanduser(playnite_games_file_path)

    # Check file exists
    if not os.path.exists(playnite_games_file_path):
        print(f"Playnite games file not found: {playnite_games_file_path}")
        return []

    # read text file as one-name-per-line. use utf-8-sig to drop a BOM if present
    with open(playnite_games_file_path, encoding='utf-8-sig') as f:
        # strip any leftover BOM and whitespace/newlines
        lines = [line.rstrip('\r\n').lstrip('\ufeff') for line in f if line.strip() != ""]
    df = pd.DataFrame({'name': lines})
    
    # Remove leading/trailing whitespace
    df['name'] = df['name'].str.strip()  
    # remove duplicates and write to list
    games = df['name'].dropna().unique().tolist()

    return games

def load_games_to_match(file_path='nucleus_games.txt'):
    """
    Load games from a text file, assume one game per line.
    """
    # Assume text file with one game per line. use utf-8-sig to handle BOMs.
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        games = [line.strip().lstrip('\ufeff') for line in f if line.strip()]
    
    return games

def fuzzy_match_games(nucleus_games, playnite_games, threshold=80, limit=3):
    """
    Fuzzy match nucleus games against playnite games.
    
    Args:
        nucleus_games: List of games to find matches for
        playnite_games: List of games to match against (your Playnite collection)
        threshold: Minimum similarity score (0-100)
        limit: Number of top matches to return
    
    Returns:
        DataFrame with matches
    """
    results = []
    
    for nucleus_game in nucleus_games:
        # Get top matches
        matches = process.extract(nucleus_game, playnite_games, scorer=fuzz.token_sort_ratio, limit=limit)
        
        # Filter by threshold
        good_matches = [(match, score) for match, score in matches if score >= threshold]
        
        if good_matches:
            for match, score in good_matches:
                results.append({
                    'nucleus_game': nucleus_game,
                    'playnite_game': match,
                    'score': score,
                    'is_top_match': score == good_matches[0][1]  # Flag the best match
                })
        else:
            # No matches found above threshold
            results.append({
                'nucleus_game': nucleus_game,
                'playnite_game': 'NO MATCH FOUND',
                'score': 0,
                'is_top_match': False
            })
    
    return pd.DataFrame(results)

def match_single_game(game_name, playnite_games, threshold=70):
    """
    Helper function to match a single game name.
    Useful for testing or interactive use.
    """

    matches = process.extract(game_name, playnite_games, scorer=fuzz.token_sort_ratio, limit=5)
    good_matches = [(match, score) for match, score in matches if score >= threshold]
    
    return good_matches