import os, disnake, requests, psycopg2, base64
from disnake.ext import tasks
from dotenv import load_dotenv
from disnake.ext import commands

load_dotenv()

bot = commands.Bot(
	intents=disnake.Intents.all(), 
	allowed_mentions=disnake.AllowedMentions(everyone=True)
)

last_cache = None

def decrypt(ciphertext_b64):
	    cipher = AES.new(os.getenv('encryption_key').encode(), AES.MODE_ECB)
	    decrypted = cipher.decrypt(base64.b64decode(ciphertext_b64))
	    pad = decrypted[-1]
	    return decrypted[:-pad].decode('utf-8')

@tasks.loop(seconds=2)
async def watcher():
	global last_cache
	db = os.getenv('db_url')
	conn = psycopg2.connect(db)
	cur = conn.cursor()

	cur.execute("SELECT id, username, first, second, third, fourth, fifth, sixth, seventh, eighth, nineth, tenth FROM public.applysubmissions ORDER BY id DESC LIMIT 1")
	row = cur.fetchone()

	cur.close()
	conn.close()
	if not row:
	    return

	if row != last_cache:
	    last_cache = row

	    (max_id, username, first, second, third, fifth, sixth, seventh, eighth, nineth, tenth) = row
	    channel = bot.get_channel(1469673733580128431)
	    decryptedMsg = decrypt(msg)
	    check = True
	    if channel:
	        for word in ["login", "register", "msg", "/give"]:
	        	if word in decryptedMsg:
	        		check = False
	        		break
	        	if check:
	        		embed = disnake.Embed(
				        title="Application",
				        url="https://adarealm.gethonis.com",
				        color=disnake.Colour.blue(),
				        timestamp=datetime.datetime.now(),
				    )

					
		        	await channel.send(embed=embed)

watcher.start()

@bot.event
async def on_ready():
	activity = disnake.Game(name="Have you applied?")
	await bot.change_presence(status=disnake.Status.idle, activity=activity)

if __name__ == "__main__":
	bot.run(os.getenv('bot_token'))