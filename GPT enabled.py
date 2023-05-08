import discord
import os
from discord.ext import commands
import openai

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.reactions = True

bot = commands.Bot(command_prefix='!', intents=intents)
openai.api_key = os.getenv('OPENAI_API_KEY')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    # print("Connected to the following guilds:") # Testing code
    # for guild in bot.guilds:
    #     print(f"{guild.name} (id: {guild.id})")


#greeting the bot
@bot.command()
async def hello(ctx):
    await ctx.send('Hello!!')


# we can ask the bot for information in this event
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("!info"):
        content = message.content[len("!info"):].strip()

        # Make a request to the OpenAI API for text summarization
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt = content,
            max_tokens=100,
            temperature=0.2,
            top_p=1.0,
            n=1,
            stop=None,
        )

        # Extract the summary from the OpenAI API response
        output = response.choices[0].text.strip()

        # Send the summary as a message in the Discord channel
        await message.channel.send(output)


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
