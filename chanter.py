import discord
import openai
import os


openai.api_key = os.environ.get("chatgpt")

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

    if client.user in message.mentions: # Check if bot was mentioned
        prompt = message.content.replace(f'<@!{client.user.id}> ', '') # Remove bot mention from prompt
        response = generate_response(prompt)
        await message.channel.send(response)

    elif message.content.startswith('!chanter'):
        prompt = message.content[9:] # Remove the "!chanter " prefix
        response = generate_response(prompt)
        await message.channel.send(response)

def generate_response(prompt):
    # Call OpenAI's API to generate a response based on the prompt
    model_engine = "text-davinci-003"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=220,
        n=1,
        stop=None,
        temperature=0.9,
    )

    return response.choices[0].text.strip()

client.run(os.environ.get("bot"))
