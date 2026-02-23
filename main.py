
from defs import *

def main():
    """
    Main function to run the fuzzy matching.
    """
    print("=== Playnite Fuzzy Game Matcher ===\n")
       
    # Get matching threshold
    try:
        threshold = int(input("\nEnter matching threshold (0-100, default 80): ") or "80")
        threshold = max(0, min(100, threshold))  # Clamp to 0-100
    except ValueError:
        threshold = 80
        print("Using default threshold: 80")
    
    print("\nLoading games...")
    
    # Load games
    nucleus_games = load_games_to_match()
    print(f"Loaded {len(nucleus_games)} games to match")
    
    playnite_games = get_playnite_games()
    print(f"Loaded {len(playnite_games)} games from Playnite")
       
    print("\nMatching games...")
    results_df = fuzzy_match_games(nucleus_games, playnite_games, threshold)
    
    # Save results
    output_file = "playnite_matches.csv"
    results_df.to_csv(output_file, index=False)
    print(f"\nResults saved to: {output_file}")
    
    # Show summary
    matched = results_df[results_df['playnite_game'] != 'NO MATCH FOUND']['nucleus_game'].nunique()
    unmatched = results_df[results_df['playnite_game'] == 'NO MATCH FOUND']['nucleus_game'].nunique()
    
    print(f"\nSummary:")
    print(f"  - Games matched: {matched}")
    print(f"  - Games not matched: {unmatched}")
    
    # Show sample of matches
    print("\nSample matches (best matches only):")
    sample = results_df[results_df['is_top_match']].head(10)
    for _, row in sample.iterrows():
        if row['playnite_game'] != 'NO MATCH FOUND':
            print(f"  {row['nucleus_game']} -> {row['playnite_game']} (Score: {row['score']})")

if __name__ == "__main__":
    # Run the main matching function
    main()