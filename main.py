import os
import discord
import use_data
from discord.ext import commands

TOKEN = 'OTYxOTIyMzI4MDAwODg0NzM3.G3DcYT.ArU5lRWsFaD5cs4YWU75tT-F8cix_NRdpNPBGM'

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

@bot.command()
async def news(ctx):
    msg = use_data.get_articles()
    await ctx.send(str(msg))


bot.run(TOKEN)
