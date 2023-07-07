from dotenv import load_dotenv
import discord
import openai
import os

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        response = generate_response(message.content)
        await message.channel.send(response)
        
    # Check if the bot is mentioned in the message
    elif client.user in message.mentions:
        response = generate_response(message.content)
        await message.channel.send(response)

def generate_response(prompt):
    # Call OpenAI's API to generate a response based on the prompt
    model_engine = "text-davinci-003"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.9,
    )

    return response.choices[0].text.strip()

client.run(os.environ.get("DISCORD_BOT_TOKEN"))
