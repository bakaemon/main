import os
from chat import ChatGPT
import discord
from dotenv import load_dotenv

load_dotenv()
client = discord.Client(intents=discord.Intents.default())
discordKey = os.getenv('DISCORD')

bot_name = "ChatGPT" # set the name of your bot here

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    chatgpt = ChatGPT(f"Your name is {bot_name}. You are a bot. You are in a Discord server. You are talking to a human through Discord. Say hello to the human!")
    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return
    
    # Remember the message by date
    mention = client.user
    if mention in message.mentions:
        target = message.author
        # Remove the mention from the message and '\n' characters, if present
        message_txt = message.content.replace(
            f'<@!{client.user.id}>', '', 1).strip()
        mention_str = "<@"  # the mention string to search for
        message_words = message_txt.split()  # split the message text into words
        clean_words = [word for word in message_words if not word.startswith(
            mention_str)]  # exclude any mention string
        # join the remaining words to form clean text
        prompt = " ".join(clean_words)
        if prompt.startswith('!rememberme'):
            chatgpt.save_history(f'{target.id}.json')
            return await message.add_reaction('👍')

        if prompt.startswith('!forgetme'):
            if os.path.exists(f'{target.id}.json'):
                os.remove(f'{target.id}.json')
            return await message.add_reaction('👍')

        if os.path.exists(f'{message.mentions[0].id}.json'):
            chatgpt.load_history(f'{target.id}.json')
        
        result = chatgpt.chat(prompt)
        if os.path.exists(f'{target.id}.json'):
            chatgpt.save_history(f'{target.id}.json')

        if result:
            output = result
            await message.channel.send(output)
        else:
            await message.channel.send('Error: ' + result['output'])

# Run the bot
client.run(discordKey)