import os

import discord
import random
import openai
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD_NAME')
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

def poemPrompt(topic):
    messages =[
        {"role": "system", "content": f"I want you to act as a poet. You will create poems that evoke emotions and have the power to stir people’s soul. Write on any topic or theme but make sure your words convey the feeling you are trying to express in beautiful yet meaningful ways. You can also come up with short verses that are still powerful enough to leave an imprint in readers' minds. "},
        {"role": "user", "content": f": My first request is 'I need a poem about {topic}'"}
        ]
    
    return messages
def customPrompt(prompt, question):
    messages =[
        {"role": "system", "content": f"{prompt}"},
        {"role": "user", "content": f"{question}'"}
        ]
    return messages
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    guild = discord.utils.get(bot.guilds, name=GUILD)    
    print(f'{bot.user} is connected to the following guild:\n'
          f'{guild.name}(id: {guild.id})'
         )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@bot.command(name='poem')
async def poem(ctx, topic):
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=poemPrompt(topic),
            temperature=0.6,
        )
    await ctx.send(response.choices[0].message.content)

@bot.command(name='custom')
async def poem(ctx, prompt, question):
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=customPrompt(prompt, question),
            temperature=0.6,
        )
    await ctx.send(response.choices[0].message.content)
@bot.command(name='roll')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))
bot.run(TOKEN)