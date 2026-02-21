import os, disnake, requests, psycopg2, base64
from disnake.ext import tasks
from Crypto.Cipher import AES
from dotenv import load_dotenv
from disnake.ext import commands

load_dotenv()

bot = commands.Bot(
	intents=disnake.Intents.all(), 
	allowed_mentions=disnake.AllowedMentions(everyone=True)
)

class ResponseApplyEmbed(disnake.ui.View):
    def __init__(self, username: str):
        super().__init__(timeout=None)
        self.username = username


    @disnake.ui.button(label="Accept", style=disnake.ButtonStyle.success, custom_id="accept_btn")
    async def button_accept_callback(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        member = disnake.utils.find(lambda m: m.name == self.username or m.display_name == self.username, interaction.guild.members)
        role = interaction.guild.get_role(1473025835404624016)

        message = ""
        if member:

        	await member.add_roles(role)

        	try:

        		await member.send("Your application was accepted!")

        	except disnake.Forbidden:

        		message="His dms are locked!"

        	await interaction.response.send_message(f"{member.mention} You've been accepted {message}", ephemeral=True)

        else:

        	await interaction.response.send_message("{self.username} is not on server, or he put wrong username", ephemeral=True)
    @disnake.ui.button(label="Deny", style=disnake.ButtonStyle.danger, custom_id="deny_btn")
    async def button_deny_callback(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
    	member = disnake.utils.find( lambda m: m.name == self.username or m.display_name == self.username, interaction.guild.members)
    	message = ""
    	if member:
    		try:

    			await member.send("You")

    		except disnake.Forbidden:

    			message = "His dms are locked!"
    		await member.kick(reason="Application denied")

    		await interaction.response.send_message(f"{member.mention} Has been denied! {message}", ephemeral=True)
        else:

        	await interaction.response.send_message(f"{self.username} could not be found!", ephemeral=True)


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

	    (max_id, username, first, second, third, fourth, fifth, sixth, seventh, eighth, nineth, tenth) = row
	    channel = bot.get_channel(1469673733580128431)
	    if channel:
	        embed = disnake.Embed(title="Application", color=disnake.Colour.blue())
	        embed.add_field(name="username", value=decrypt(username), inline=False)
	        embed.add_field(name="What is your Minecraft username?", value=decrypt(first), inline=False)
	        embed.add_field(name="What Minecraft do you use?", value=decrypt(second), inline=False)
	        embed.add_field(name="How old are you?", value=decrypt(third), inline=False)
	        embed.add_field(name="What is your timezone?", value=decrypt(fourth), inline=False)
	        embed.add_field(name="Why do you want to join our community?", value=decrypt(fifth), inline=False)

	        embed.add_field(name="Are you okay with a 2-day trial period before becoming a full member?", value=decrypt(sixth), inline=False)
	        embed.add_field(name="What are your main interests if you do join the server and what would you bring to our community?", value=decrypt(seventh), inline=False)
	        embed.add_field(name="What does a 'healthy community' mean to you?", value=decrypt(eighth), inline=False)
	        embed.add_field(name="Tell us a little bit about yourself. (for example: hobbies, work, pets etc.)", value=decrypt(nineth), inline=False)
	        embed.add_field(name="What was rule number 5 in our server rules section?", value=decrypt(tenth), inline=False)
	        usernamedec = decrypt(username)
	        
	        await channel.send(embed=embed, view=ResponseApplyEmbed(usernamedec))

watcher.start()

@bot.event
async def on_ready():
	activity = disnake.Game(name="Have you applied?")
	await bot.change_presence(status=disnake.Status.idle, activity=activity)

if __name__ == "__main__":
	bot.run(os.getenv('bot_token'))