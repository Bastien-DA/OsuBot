import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)


@bot.tree.command(name="test",
                  description="its a test command",)
async def slash_command(interaction: discord.Interaction):
    embed = discord.Embed(title="Test Command")
    embed.add_field(name="bastou", value="je teste les slash commands")
    await interaction.response.send_message(embed=embed)


@bot.event
async def on_ready():
    await bot.tree.sync()


bot.run(TOKEN)
