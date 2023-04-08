import discord
import openai
import os


openai.api_key = os.environ.get("chatgpt")

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

previous_messages = {}

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # Get the user's ID
    user_id = message.author.id

    if isinstance(message.channel, discord.DMChannel):
        response = generate_response(message.content, user_id)
        await message.channel.send(response)
        
    # Check if the bot is mentioned in the message
    elif client.user in message.mentions:
        response = generate_response(message.content, user_id)
        await message.channel.send(response)

def generate_response(prompt, user_id):
    
    # Get the user's previous message
    previous_message = previous_messages.get(user_id, "")
    
    # Combine the previous message and the current prompt
    prompt = f"{previous_message} {prompt}" if previous_message else prompt
    
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
    
    # Save the current message as the user's previous message
    previous_messages[user_id] = prompt

    return response.choices[0].text.strip()

client.run(os.environ.get("bot"))
