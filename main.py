import os
import discord

class Client(discord.Client):
    async def on_ready(self):
        print(f'logged on as {self.user}!')

    async def on_message(self, message):
        if message.author.bot:
            return

        #print(f'Message from {message.author}: {message.content}')
        if message.content.startswith('!wiki'):
            await message.channel.send('https://ship-community-valrus.fandom.com/wiki/Main_Page')

intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run(os.environ["DISCORD_TOKEN"])