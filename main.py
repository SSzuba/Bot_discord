import os
import discord
import get_data
from discord.ext import commands

TOKEN = 'OTYxOTIyMzI4MDAwODg0NzM3.YlAB-g.jEsaYZnYSLJL-e2474pHd0pCB7k'

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f'{bot.user} succesfully logged in!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content == 'help':
        messagee = message.content.split('\n')
        output_text = '\n'.join(('test_start' + line + 'test_end') for line in messagee)
        await message.channel.send(output_text)

    

    await bot.process_commands(message)


# Start each command with the @bot.command decorater
@bot.command()
async def square(ctx, arg): # The name of the function is the name of the command
    print(arg) # this is the text that follows the command
    await ctx.send(int(arg) ** 2) # ctx.send sends text in chat


bot.run(TOKEN)
