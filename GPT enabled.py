import discord
import os
from discord.ext import commands
import openai

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.reactions = True

bot = commands.Bot(command_prefix='!', intents=intents)
openai.api_key = 'OPENAI_API_KEY'

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    # print("Connected to the following guilds:") # Testing code
    # for guild in bot.guilds:
    #     print(f"{guild.name} (id: {guild.id})")

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

@bot.command()
async def info(ctx, *, message):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=message,
        temperature=0.7,
        max_tokens=50
    )
    await ctx.send(response.choices[0].text)
  



try:
    bot.run(os.getenv("TOKEN"))
except discord.HTTPException as e:
    if e.status == 429:
        print(
            "The Discord servers denied the connection for making too many requests"
        )
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
        )
    else:
        raise e
