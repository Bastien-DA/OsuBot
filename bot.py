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
        embed.set_author(name=f"{user_info['username']}", icon_url=f"https://a.ppy.sh/{user_info['user_id']}")
        embed.add_field(name="Join Date", value=f"{user_info['join_date']}", inline=False)
        embed.add_field(name="Rank", value=f"pp rank: {user_info['pp_rank']}"
                                           f" and country rank: {user_info['pp_country_rank']}"
                                           f" {user_info['country']}", inline=False)
        embed.add_field(name="Accuracy", value=f"{user_info['accuracy']} %", inline=False)
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
    await interaction.response.send_message("This command is not implemented yet")


@bot.event
async def on_ready():
    await bot.tree.sync()


bot.run(TOKEN)
