# Anilist Data Fetching_ Discord bot

This bot allows you to fetch and display information from AniList about users, including their statistics and favorites. It's built using Python, the discord.py library, and the AniList GraphQL API.

# Features

Fetch Basic User Info: Retrieve and display basic information about a user, including their profile description, avatar, and profile URL.
Anime Statistics: Get statistics about the anime a user has watched, such as the total count, mean score, and total minutes watched.
Manga Statistics: Get statistics about the manga a user has read, such as the total count, mean score, and total chapters read.
Favourites: Retrieve and display a user's favorite anime, manga, characters, and staff.
Custom Help Command: A dedicated help command to list all available commands and their usage.

# Commands

!anilist_basic (username) : Fetch and display basic information about the specified AniList user.

!anilist_anime_stats (username) : Fetch and display the anime statistics of the specified AniList user.

!anilist_manga_stats (username) : Fetch and display the manga statistics of the specified AniList user.

!anilist_favourites (username) : Fetch and display the favorite anime, manga, characters, and staff of the specified AniList user.

!help: Display a list of available commands and their descriptions.

# Setup

Clone the repository:

```bash
git clone https://github.com/GraveEaterMadison/anilist_data_fetching_discord_bot.git

cd anilist_data_fetching_bot

```
# Install the required packages:

pip install discord.py requests

# Set your Discord bot token and owner ID:

Replace 'Your Bot Token' in the 'Your Bot Token' line with your actual Discord bot token.
Replace 'Your Discord ID' in the OWNER_ID variable with your Discord user ID.


# Run the bot:

python bot.py
