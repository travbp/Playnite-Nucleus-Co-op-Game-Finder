# Setup

## Get list of supported games in Nucleus Coop

- Create file called nucleus_games.txt in project root (version in repo was created 2/22/2026)

- Copy [list of supported games from reddit](https://www.reddit.com/r/nucleuscoop/comments/opu0eg/list_of_nucleus_coop_supported_games/) post into file

- Cleanup:

```bash
# Bash
# Run this to remove empty lines
tmp=$(mktemp) && sed '/./!d' nucleus_games.txt > "$tmp" && mv "$tmp" nucleus_games.txt
```



## Get list of game names in Playnite Library

- Start a PowerShell instance with pre-loaded Playnite SDK from main menu -> Extensions -> Interactive SDK PowerShell. This will open PowerShell console connected to Playnite process and initialize new runspace for this interactive session.


- Run the following in the opened PowerShell terminal:

```powershell
# initialize basic Playnite SDK variables
$PlayniteRunspace = Get-Runspace -Name 'PSInteractive'
$PlayniteApi = $PlayniteRunspace.SessionStateProxy.GetVariable('PlayniteApi')

# get names of all games in playnite library
$games = $PlayniteApi.Database.Games.Name

# writes list of game names to a text file in user root directory
Set-Content -Path '~\games.txt' -Value $games -Encoding UTF8
```

## Make virtual environment for python script

```bash
#Bash

# create and activate venv
python -m venv .venv && source .venv/Scripts/activate

# install dependencies
pip install -r requirements.txt

```

# Usage

```bash
# Bash

# activate venv
source .venv/Scripts/activate

# run python script
python main.py
```