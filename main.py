
from defs import *

def main():
    """
    Main function to run the fuzzy matching.
    """
    print("=== Playnite Fuzzy Game Matcher ===\n")
    
    # Get input file path
    while True:
        input_file = input("Enter path to your game list file (CSV or TXT): ").strip('"').strip()
        if os.path.exists(input_file):
            break
        print("File not found. Please try again.")
    
    # Get Playnite database path
    try:
        db_path = connect_to_playnite_games_db()
        print(f"Found Playnite database at: {db_path}")
    except FileNotFoundError as e:
        print(e)
        db_path = input("Please enter the path to your Playnite library.db file: ").strip('"').strip()
    
    # Get matching threshold
    try:
        threshold = int(input("\nEnter matching threshold (0-100, default 80): ") or "80")
        threshold = max(0, min(100, threshold))  # Clamp to 0-100
    except ValueError:
        threshold = 80
        print("Using default threshold: 80")
    
    print("\nLoading games...")
    
    # Load games
    source_games = load_games_to_match(input_file)
    print(f"Loaded {len(source_games)} games to match")
    
    playnite_games = get_playnite_games(db_path)
    print(f"Loaded {len(playnite_games)} games from Playnite")
    
    if not playnite_games:
        print("No games found in Playnite database. Exiting.")
        return
    
    print("\nMatching games...")
    results_df = fuzzy_match_games(source_games, playnite_games, threshold)
    
    # Save results
    output_file = "playnite_matches.csv"
    results_df.to_csv(output_file, index=False)
    print(f"\nResults saved to: {output_file}")
    
    # Show summary
    matched = results_df[results_df['Matched_Game'] != 'NO MATCH FOUND']['Source_Game'].nunique()
    unmatched = results_df[results_df['Matched_Game'] == 'NO MATCH FOUND']['Source_Game'].nunique()
    
    print(f"\nSummary:")
    print(f"  - Games matched: {matched}")
    print(f"  - Games not matched: {unmatched}")
    
    # Show sample of matches
    print("\nSample matches (best matches only):")
    sample = results_df[results_df['Is_Top_Match']].head(10)
    for _, row in sample.iterrows():
        if row['Matched_Game'] != 'NO MATCH FOUND':
            print(f"  {row['Source_Game']} -> {row['Matched_Game']} (Score: {row['Score']})")

if __name__ == "__main__":
    # Run the main matching function
    main()
    
    # Uncomment below for a quick test:
    # test_games = ["The Witcher 3", "Cyberpunk 2077", "Mario Kart", "Nonexistent Game"]
    # db_path = connect_to_playnite_games_db()
    # playnite_games = get_playnite_games(db_path)
    # for game in test_games:
    #     matches = match_single_game(game, playnite_games)
    #     print(f"\n{game}:")
    #     for match, score in matches:
    #         print(f"  -> {match} ({score})")