import os, disnake, requests, psycopg2, base64
from disnake.ext import tasks
from dotenv import load_dotenv
from disnake.ext import commands

load_dotenv()

bot = commands.Bot(
	intents=disnake.Intents.all(), 
	allowed_mentions=disnake.AllowedMentions(everyone=True)
)
@bot.event
async def on_ready():
	activity = disnake.Game(name="Have you applied?")
	await bot.change_presence(status=disnake.Status.idle, activity=activity)

if __name__ == "__main__":
	bot.run(os.getenv('bot_token'))