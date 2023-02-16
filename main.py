import discord
import sqlite3
import re
import asyncio
from difflib import SequenceMatcher
from discord.ext import commands, tasks
from discord.utils import get
from urllib.parse import urlparse


TOKEN = 'TOKEN'

bot = commands.Bot(intents=discord.Intents.all(), command_prefix="!")
con = sqlite3.connect("database.db")
cur = con.cursor()
started_tasks = []
url_pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"


async def get_news(channel, typ, new, update):
    new_checker = count(typ, "New")
    update_checker = count(typ, "Update")
    while True:
        if new_checker > new:
            diff = new_checker - new
            res2 = cur.execute(
                f'SELECT title, url, type, status FROM articles WHERE type is "{typ}" and status is "New" LIMIT {diff} OFFSET {new}')
            for row in res2.fetchall():
                await channel.send('NEW! ' + row[0] + ' ' + row[1])
                new += 1
            await asyncio.sleep(10)
        elif update_checker > update:
            diff = update_checker - update
            res2 = cur.execute(
                f'SELECT title, url, type, status FROM articles WHERE type is "{typ}" and status is "Update" LIMIT {diff} OFFSET {update}')
            for row in res2.fetchall():
                await channel.send('UPDATE! ' + row[0] + ' ' + row[1])
                update += 1
            await asyncio.sleep(10)
        else:
            new_checker = count(typ, "New")
            update_checker = count(typ, "Update")
            await asyncio.sleep(10)

def count(typ, status):
    res = cur.execute(
        f'SELECT url, type, status FROM articles WHERE type is "{typ}" and status is "{status}"')
    counter = 0
    for row in res.fetchall():
        counter += 1
    return counter


@bot.event
async def on_ready():
    print(f'{bot.user} succesfully logged in!')


@bot.command(name='follow', help='!follow type - start follow news type on private channel nick-type')
async def follow(ctx, arg):
    founded = False
    guild = ctx.guild
    member = ctx.author
    admin_role = get(guild.roles, name="Admin")
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member: discord.PermissionOverwrite(read_messages=True),
        admin_role: discord.PermissionOverwrite(read_messages=True)
    }
    channel_name = str(member) + ' ' + str(arg)
    channel_name = channel_name.replace(" ", "-").lower().replace("#", "")
    if arg == "sport" or arg == "moto" or arg == "biznes":
        for channel in ctx.guild.channels:
            if channel.name == channel_name:
                await ctx.send("You already follow " + arg + " newses.")
                founded = True
                break
        if founded is False:
            await ctx.guild.create_text_channel(channel_name, overwrites=overwrites)
            await ctx.send('you start follow ' + arg + ' newses!')
            for channel in ctx.guild.channels:
                if channel.name == channel_name:
                    new = count(str(arg), "New")
                    update = count(str(arg), "Update")
                    await get_news(channel, arg, new, update)
                    break
    else:
        await ctx.send("Invalid type! You can follow sport, biznes or moto types.")


@bot.command(name='unfollow', help='!unfollow type - stop follow news type')
async def unfollow(ctx, arg):
    deleted = False
    guild = ctx.guild
    member = ctx.author
    channel_name = str(member) + ' ' + str(arg)
    channel_name = channel_name.replace(" ", "-").lower().replace("#", "")
    for channel in ctx.guild.channels:
        if channel.name == channel_name:
            await ctx.send("You stop follow " + arg + " newses.")
            await channel.delete()
            deleted = True
            break
        else:
            deleted = False
    if deleted is False:
        await ctx.send("You don't follow this type!")


@bot.command(name='add_site', help='!add_site url type - users with admin permission can add news sites.')
@commands.has_permissions(administrator=True)
async def add_site(ctx, arg1, arg2):
    founded = False
    site = str(arg1)
    if site[-1] == "/":
        site = "".join(site.rsplit(site[-1:], 1))
    res = cur.execute(f'SELECT url FROM sites')
    for row in res.fetchall():
        if row[0] == site:
            founded = True
            break
    if arg2 == "sport" or arg2 == "moto" or arg2 == "biznes":
        if founded is True:
            await ctx.send(f'{site} already added!')
        elif re.match(url_pattern, site) and founded is False:
            cur.execute('INSERT INTO sites VALUES (?, ?)', (site, arg2))
            con.commit()
            await ctx.send("You added new site " + site)
        else:
            await ctx.send("Wrong URL! Example: https://site.pl")
    else:
        await ctx.send("Invalid type! You can add sport, biznes or moto types site.")


@bot.command(name='rem_site', help='!add_site url - users with admin permission can remove news sites.')
@commands.has_permissions(administrator=True)
async def rem_site(ctx, arg):
    founded = False
    site = str(arg)
    res = cur.execute(f'SELECT url FROM sites')
    if site[-1] == "/":
        site = "".join(site.rsplit(site[-1:], 1))
    for row in res.fetchall():
        if row[0] == site:
            founded = True
            break
    if founded is True:
        cur.execute(f'DELETE FROM sites WHERE url = "{site}"')
        con.commit()
        await ctx.send(f'You deleted {site} from database!')
    else:
        await ctx.send('This site is not in database!')


@bot.command(name='search', help='!search text - you can search newest article having typed text in title.')
async def search(ctx, *args):
    res = cur.execute("SELECT title, url, date FROM articles")
    founded = False
    match_counter = 0
    counter_words = 0
    counter_args = 0
    param = ''
    for a in args:
        param += a + ' '
        counter_args += 1
    await ctx.send("Looking for newest: " + param + "article")
    param_list = param.split()
    for row in reversed(res.fetchall()):
        title = str(row[0]).lower()
        url = str(row[1])
        date = str(row[2])
        url_parse = urlparse(url)
        url_parse = str(url_parse.path).replace("-", " ").replace("/", " ")
        check_text = title + " " + url_parsez
        check_list = check_text.split()
        for p in param_list:
            for c in check_list:
                matcher = SequenceMatcher(None, p, c).ratio()
                if matcher > 0.8:
                    counter_words += 1
                    match_counter += matcher        
            if match_counter != 0 and counter_words != 0:
                sim = match_counter / counter_words
            else:
                sim = 0
        if sim > 0.8 and counter_words >= counter_args:
            await ctx.send(date + ": " + title + " " + url)
            founded = True
            break
    if founded is False:
        await ctx.send("No articles!")


@bot.command(name='show_sites', help='!show_sites - you can check news sites.')
async def show_sites(ctx):
    msg = '```\n'
    res = cur.execute("SELECT url, type FROM sites")
    for row in res.fetchall():
        msg += row[0] + " - " + row[1] + "\n"
    msg += '```'
    await ctx.send(msg)


@bot.command(name='show_types', help='!show_types - you can check news types.')
async def show_types(ctx):
    msg = '```\n'
    res = cur.execute("SELECT type FROM sites GROUP BY type")
    for row in res.fetchall():
        msg += str(row[0]) + "\n"
    msg += '```'
    await ctx.send(msg)

bot.run(TOKEN)
