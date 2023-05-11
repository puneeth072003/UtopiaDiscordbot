import discord
import os
from discord.ext import commands
import openai
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.reactions = True
intents.typing = False
intents.presences = False

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

        # Perform the summarization
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
            
            content = target_message.content
          
            # Perform the summarization
            summary = summarize(content)

            # Send the summarized message as a response
            await message.channel.send(f"Summary of Message ID {message_id}: {summary}")

        except discord.NotFound:
            await message.channel.send(f"Message with ID {message_id} not found.")

    await bot.process_commands(message)
  
#######################################################

@bot.command()
async def question(ctx, *, question):
    channel = ctx.channel

    # Fetch the channel conversation history
    messages = []

    async for msg in channel.history(limit=20):
        messages.append(msg)

    # Reverse the order of messages to process them from oldest to newest
    messages.reverse()

    # Concatenate the conversation text
    conversation = '\n'.join([f'{msg.author.name}: {msg.content}' for msg in messages])

    # Generate a response from OpenAI GPT-3.5 Turbo (using v1/chat/completions endpoint)
    # Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=f"Go through these texts and provide an answer for the given question:\n{conversation}\nQuestion: {question}",
        max_tokens=100,
        temperature=0.3,
        top_p=1.0,
        n=1,
        stop=None,
    )

    # Extract the generated answer
    answer = response.choices[0].text.strip()

    # Send the answer as a response
    await ctx.send(answer)

#######################################################
@bot.command()
@commands.has_permissions(administrator=True)
async def summarize_day(ctx):
  try:
    # Define the channel names to include in the summarization
    channel_names = ["test", "test-2"]

    # Calculate the start and end date for the past day
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)

    # Iterate over the channels
    for channel_name in channel_names:
        channel = discord.utils.get(ctx.guild.channels, name=channel_name)

        if channel:
            concatenated_text = ""

            # Fetch the messages within the specified timeframe
            async for message in channel.history(limit=None, after=start_date, before=end_date):
                concatenated_text += message.content + " "

            # Perform the summarization 
            summary = data(concatenated_text)

            # Send the summarized message as a response
            await ctx.send(f"Summary of {channel_name} channel:\n{summary}")


  except Exception:
    await ctx.send("Content to be summarized too large")
##################################################
@bot.command()
@commands.has_permissions(administrator=True)
async def summarize_week(ctx):
  try:
    # Define the channel names to include in the summarization
    channel_names = ["test", "test-2"]

    # Calculate the start and end date for the past day
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    # Iterate over the channels
    for channel_name in channel_names:
        channel = discord.utils.get(ctx.guild.channels, name=channel_name)

        if channel:
            concatenated_text = ""

            # Fetch the messages within the specified timeframe
            async for message in channel.history(limit=None, after=start_date, before=end_date):
                concatenated_text += message.content + " "

            # Perform the summarization 
            summary = data(concatenated_text)

            # Send the summarized message as a response
            await ctx.send(f"Summary of {channel_name} channel:\n{summary}")


  except Exception:
    await ctx.send("Content to be summarized too large")
    
##################################################
@bot.command()
@commands.has_permissions(administrator=True)
async def summarize_month(ctx):
  try:
    # Define the channel names to include in the summarization
    channel_names = ["test", "test-2"]

    # Calculate the start and end date for the past day
    end_date = datetime.now()
    start_date = end_date - timedelta(days=31)

    # Iterate over the channels
    for channel_name in channel_names:
        channel = discord.utils.get(ctx.guild.channels, name=channel_name)

        if channel:
            concatenated_text = ""

            # Fetch the messages within the specified timeframe
            async for message in channel.history(limit=None, after=start_date, before=end_date):
                concatenated_text += message.content + " "

            # Perform the summarization 
            summary = data(concatenated_text)

            # Send the summarized message as a response
            await ctx.send(f"Summary of {channel_name} channel:\n{summary}")


  except Exception:
    await ctx.send("Content to be summarized too large")

##################################################
def summarize(text):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=f"Summarize the following content {text} up to 2-3 sentences",
        max_tokens=100,
        temperature=0.3,
        top_p=1.0,
        n=1,
        stop=None,
    )

    return response.choices[0].text.strip()
##############################################
def data(text):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=f"Please provide the most shortened summary of following text:  {text}",
        max_tokens=len(text),
        temperature=0.3,
        top_p=1.0,
        n=1,
        stop=None,
    )

    return response.choices[0].text.strip()
################################################
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
######################################################
