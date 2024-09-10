import discord
from discord.ext import commands
import requests
import re


intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

 
OWNER_ID = 'Your_Discord_ID'

TOKEN = 'Your_bot_token'

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    owner = await bot.fetch_user(OWNER_ID)
    if owner:
        await owner.send('Anilist data Script is active')
    else:
        print(f"Could not find user with ID {OWNER_ID}")


ANILIST_USER_QUERY = '''
query ($name: String) {
    User(name: $name) {
        id
        name
        about
        avatar {
            large
        }
        statistics {
            anime {
                count
                meanScore
                minutesWatched
            }
            manga {
                count
                meanScore
                chaptersRead
            }
        }
        favourites {
            anime {
                nodes {
                    title {
                        romaji
                    }
                }
            }
            manga {
                nodes {
                    title {
                        romaji
                    }
                }
            }
            characters {
                nodes {
                    name {
                        full
                    }
                }
            }
            staff {
                nodes {
                    name {
                        full
                    }
                }
            }
        }
        siteUrl
        updatedAt
    }
}
'''

def fetch_anilist_user_data(username: str):
    url = 'https://graphql.anilist.co'
    variables = {'name': username}
    response = requests.post(url, json={'query': ANILIST_USER_QUERY, 'variables': variables})
    response.raise_for_status()
    return response.json().get('data', {}).get('User')

def clean_about_text(text: str):
    text = text.replace('<b>', '**').replace('</b>', '**')
    image_urls = re.findall(r'~img\d+\((.*?)\)~', text)
    for url in image_urls:
        text = text.replace(f'~img500({url})~', f'\n![image]({url})\n')
    text = re.sub(r'<.*?>', '', text)
    return text

def split_text(text, max_length):
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

def split_embed(embed, title):
    MAX_EMBED_SIZE = 6000
    embeds = []
    current_embed = discord.Embed(title=title)
    for field in embed.fields:
        if len(current_embed) + len(field.name) + len(field.value) >= MAX_EMBED_SIZE:
            embeds.append(current_embed)
            current_embed = discord.Embed(title=title)
        current_embed.add_field(name=field.name, value=field.value, inline=field.inline)
    embeds.append(current_embed)
    return embeds

@bot.command()
async def anilist_basic(ctx, username: str):
    try:
        data = fetch_anilist_user_data(username)
        if data:
            about_text = clean_about_text(data['about'] or "No description")
            about_chunks = split_text(about_text, 1024)
            for idx, chunk in enumerate(about_chunks):
                embed = discord.Embed(title=data['name'], url=data['siteUrl'])
                if idx == 0:
                    embed.set_thumbnail(url=data['avatar']['large'])
                embed.add_field(name="Description", value=chunk, inline=False)
                if idx == len(about_chunks) - 1:
                    embed.add_field(name="Profile URL", value=data['siteUrl'], inline=False)
                    embed.add_field(name="Last Updated", value=data['updatedAt'], inline=False)
                await ctx.send(embed=embed)
        else:
            await ctx.send(f"User '{username}' not found.")
    except requests.exceptions.RequestException as e:
        await ctx.send(f"Error fetching data from AniList: {e}")
    except KeyError:
        await ctx.send("Unexpected response structure from AniList.")
    except Exception as e:
        await ctx.send(f"An error occurred while processing the AniList response: {e}")

@bot.command()
async def anilist_anime_stats(ctx, username: str):
    try:
        data = fetch_anilist_user_data(username)
        if data:
            anime_stats = data['statistics']['anime']
            embed = discord.Embed(title=f"{data['name']}'s Anime Stats")
            embed.add_field(name="Anime Count", value=anime_stats['count'], inline=True)
            embed.add_field(name="Mean Score", value=anime_stats['meanScore'], inline=True)
            embed.add_field(name="Minutes Watched", value=anime_stats['minutesWatched'], inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"User '{username}' not found.")
    except requests.exceptions.RequestException as e:
        await ctx.send(f"Error fetching data from AniList: {e}")
    except KeyError:
        await ctx.send("Unexpected response structure from AniList.")
    except Exception as e:
        await ctx.send(f"An error occurred while processing the AniList response: {e}")

@bot.command()
async def anilist_manga_stats(ctx, username: str):
    try:
        data = fetch_anilist_user_data(username)
        if data:
            manga_stats = data['statistics']['manga']
            embed = discord.Embed(title=f"{data['name']}'s Manga Stats")
            embed.add_field(name="Manga Count", value=manga_stats['count'], inline=True)
            embed.add_field(name="Mean Score", value=manga_stats['meanScore'], inline=True)
            embed.add_field(name="Chapters Read", value=manga_stats['chaptersRead'], inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"User '{username}' not found.")
    except requests.exceptions.RequestException as e:
        await ctx.send(f"Error fetching data from AniList: {e}")
    except KeyError:
        await ctx.send("Unexpected response structure from AniList.")
    except Exception as e:
        await ctx.send(f"An error occurred while processing the AniList response: {e}")

@bot.command()
async def anilist_favourites(ctx, username: str):
    try:
        data = fetch_anilist_user_data(username)
        if data:
            favourites = data['favourites']
            fav_anime = ', '.join([anime['title']['romaji'] for anime in favourites['anime']['nodes']])
            fav_manga = ', '.join([manga['title']['romaji'] for manga in favourites['manga']['nodes']])
            fav_characters = ', '.join([character['name']['full'] for character in favourites['characters']['nodes']])
            fav_staff = ', '.join([staff['name']['full'] for staff in favourites['staff']['nodes']])

            embed = discord.Embed(title=f"{data['name']}'s Favourites")
            embed.add_field(name="Favourite Anime", value=fav_anime or "None", inline=False)
            embed.add_field(name="Favourite Manga", value=fav_manga or "None", inline=False)
            embed.add_field(name="Favourite Characters", value=fav_characters or "None", inline=False)
            embed.add_field(name="Favourite Staff", value=fav_staff or "None", inline=False)

            embeds = split_embed(embed, f"{data['name']}'s Favourites")
            for e in embeds:
                await ctx.send(embed=e)
        else:
            await ctx.send(f"User '{username}' not found.")
    except requests.exceptions.RequestException as e:
        await ctx.send(f"Error fetching data from AniList: {e}")
    except KeyError:
        await ctx.send("Unexpected response structure from AniList.")
    except Exception as e:
        await ctx.send(f"An error occurred while processing the AniList response: {e}")

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="AniList Bot Commands", description="Here are the commands you can use:")
    embed.add_field(name="!anilist_basic <username>", value="Fetch basic information about an AniList user.", inline=False)
    embed.add_field(name="!anilist_anime_stats <username>", value="Fetch anime statistics of an AniList user.", inline=False)
    embed.add_field(name="!anilist_manga_stats <username>", value="Fetch manga statistics of an AniList user.", inline=False)
    embed.add_field(name="!anilist_favourites <username>", value="Fetch favourite anime, manga, characters, and staff of an AniList user.", inline=False)
    embed.set_footer(text="Replace <username> with the AniList username you want to look up.")
    await ctx.send(embed=embed)

bot.run(TOKEN)
