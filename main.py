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
concatenated_text = ""


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    # print("Connected to the following guilds:") # Testing code
    # for guild in bot.guilds:
    #     print(f"{guild.name} (id: {guild.id})")


# we can ask the bot for information in this event
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

    if message.content.startswith("!info"):
        content = message.content[len("!info"):].strip()

        # Make a request to the OpenAI API for text summarization
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=content,
            max_tokens=100,
            temperature=0.2,
            top_p=1.0,
            n=1,
            stop=None,
        )

        # Extract the info from the OpenAI API response
        output = response.choices[0].text.strip()

        # Send the info as a message in the Discord channel
        await message.channel.send(output)
      
#########################################################
  
    if message.content.startswith("!shorten"):
        # Extract the message to be summarized
        content = message.content[len("!shorten"):].strip()

        # Perform the summarization using your preferred method (e.g., OpenAI API, Gensim, etc.)
        summary = summarize(content)

        # Send the summarized message as a response
        await message.channel.send(f"Summary: {summary}")

    await bot.process_commands(message)

########################################################
  
    if message.content.startswith("!summarize"):
        # Extract the message ID from the command
        message_id = message.content[len("!summarize"):].strip()

        try:
            # Fetch the message based on the provided ID
            target_message = await message.channel.fetch_message(int(message_id))
            
            # Perform the summarization using your preferred method (e.g., OpenAI API, Gensim, etc.)
            content = target_message.content
            summary = summarize(content)

            # Send the summarized message as a response
            await message.channel.send(f"Summary of Message ID {message_id}: {summary}")

        except discord.NotFound:
            await message.channel.send(f"Message with ID {message_id} not found.")

    await bot.process_commands(message)

#######################################################













def summarize(text):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=f"Summarize tthe following content {text} up to 2-3 sentences",
        max_tokens=100,
        temperature=0.3,
        top_p=1.0,
        n=1,
        stop=None,
    )

    return response.choices[0].text.strip()


##############################################
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
