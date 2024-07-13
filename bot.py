import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

import osuApi

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)


@bot.tree.command(name="get_user",
                  description="Get a user from Osu !",)
async def user(interaction: discord.Interaction, username: str):
    user_info, best_beatmpap, beatmap_info = osuApi.get_user(username)
    if user_info == "User not found":
        await interaction.response.send_message(f"User {username} not found")
    else:
        embed = discord.Embed()
        embed.set_author(name=f"{user_info['username']}")
        embed.set_thumbnail(url=f"https://a.ppy.sh/{user_info['user_id']}")
        embed.add_field(name="Level", value=f"{round(float(user_info['level']), 1)}", inline=True)
        embed.add_field(name="Join Date", value=f"{user_info['join_date']}", inline=False)
        embed.add_field(name="Mondial Rank", value=f"{user_info['pp_rank']}")
        embed.add_field(name="Country Rank", value=f"{user_info['pp_country_rank']} {user_info["country"]}")
        embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.add_field(name="SS", value=f"{user_info['count_rank_ss']}", inline=True)
        embed.add_field(name="S", value=f"{user_info['count_rank_s']}", inline=True)
        embed.add_field(name="A", value=f"{user_info['count_rank_a']}", inline=True)
        embed.add_field(name="Accuracy", value=f"{round(float(user_info['accuracy']), 2)} %", inline=False)
        embed.add_field(name="Best Map", value=f"[{beatmap_info["title"]}]"
                                               f"(https://osu.ppy.sh/beatmaps/{best_beatmpap["beatmap_id"]}) "
                                               f"{beatmap_info["artist"]}", inline=False)
        embed.add_field(name="Score", value=f"{best_beatmpap['score']}", inline=True)
        embed.add_field(name="Combo", value=f"{best_beatmpap['maxcombo']}/{beatmap_info['max_combo']}", inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.add_field(name="PP", value=f"{round(float(best_beatmpap['pp']), 2)} pp", inline=True)
        embed.add_field(name="Rank", value=f"{best_beatmpap['rank']}", inline=True)
        embed.add_field(name="Date", value=f"{best_beatmpap['date']}", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="compare",
                  description="Compare two users from Osu !")
async def compare(interaction: discord.Interaction, username1: str, username2: str):
    user_info1, user_info2, compare_info = osuApi.compare(username1, username2)
    embed = discord.Embed()
    embed.set_author(name=f"{user_info1['username']} vs {user_info2['username']}")
    embed.add_field(name=f"Level {user_info1['username']}", value=f"{round(float(user_info1['level']), 1)}", inline=True)
    embed.add_field(name=f"{compare_info['better_level']} Better", value=f"{round(float(compare_info['level']), 1)}", inline=True)
    embed.add_field(name=f"Level {user_info2['username']}", value=f"{round(float(user_info2['level']), 1)}", inline=True)
    embed.add_field(name=f"Mondial Rank {user_info1['username']}", value=f"{user_info1['pp_rank']}", inline=True)
    embed.add_field(name=f"{compare_info['better_pp_rank']} Better", value=f"{compare_info['pp_rank']}", inline=True)
    embed.add_field(name=f"Mondial Rank {user_info2['username']}", value=f"{user_info2['pp_rank']}", inline=True)
    embed.add_field(name=f"Country Rank {user_info1['username']}", value=f"{user_info1['pp_country_rank']} {user_info1['country']}", inline=True)
    embed.add_field(name=f"{compare_info['better_pp_country_rank']} Better", value=f"{compare_info['pp_country_rank']}", inline=True)
    embed.add_field(name=f"Country Rank {user_info2['username']}", value=f"{user_info2['pp_country_rank']} {user_info2['country']}", inline=True)
    embed.add_field(name=f"SS {user_info1['username']}", value=f"{user_info1['count_rank_ss']}", inline=True)
    embed.add_field(name=f"{compare_info['better_count_rank_ss']} Better", value=f"{compare_info['count_rank_ss']}", inline=True)
    embed.add_field(name=f"SS {user_info2['username']}", value=f"{user_info2['count_rank_ss']}", inline=True)
    embed.add_field(name=f"S {user_info1['username']}", value=f"{user_info1['count_rank_s']}", inline=True)
    embed.add_field(name=f"{compare_info['better_count_rank_s']} Better", value=f"{compare_info['count_rank_s']}", inline=True)
    embed.add_field(name=f"S {user_info2['username']}", value=f"{user_info2['count_rank_s']}", inline=True)
    embed.add_field(name=f"A {user_info1['username']}", value=f"{user_info1['count_rank_a']}", inline=True)
    embed.add_field(name=f"{compare_info['better_count_rank_a']} Better", value=f"{compare_info['count_rank_a']}", inline=True)
    embed.add_field(name=f"A {user_info2['username']}", value=f"{user_info2['count_rank_a']}", inline=True)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.event
async def on_ready():
    await bot.tree.sync()


bot.run(TOKEN)
