import discord
import sqlite3
import re
import asyncio
from difflib import SequenceMatcher
from discord.ext import commands, tasks
from discord.utils import get

TOKEN = 'OTYxOTIyMzI4MDAwODg0NzM3.GqVYCG.MkZgyTzwkNyZ0vljgaQOhfBKg4hdhppWAeAtN0'

bot = commands.Bot(intents=discord.Intents.all(), command_prefix="!")
con = sqlite3.connect("database.db")
cur = con.cursor()
started_tasks = []
url_pattern = "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$"


def task_generator(channel, type, new, update):
    t = tasks.loop(seconds=10)(get_news)
    started_tasks.append(t)
    t.start(channel, type, new, update)


async def get_news(channel, type, new_counter, update_counter):
    new = cur.execute(
        f'SELECT title, url, status FROM articles WHERE type is "{type}" and status is "New"')
    update = cur.execute(
        f'SELECT title, url, status FROM articles WHERE type is "{type}" and status is "Update"')
    count_new = count(type, "New")
    count_update = count(type, "Update")
    await checker(channel, type, count_new, new_counter, "New")
    new_counter = count_new
    await checker(channel, type, count_update, update_counter, "Update")
    update_counter = count_update


async def checker(channel, type, count, counter, status):
    if count > counter:
        diff = count - counter
        res2 = cur.execute(
            f'SELECT title, url, status FROM articles WHERE type is "{type}" and status is "{status}" LIMIT {diff} OFFSET {counter}')
        for row in res2.fetchall():
            await channel.send(status + '! ' + row[0] + ' ' + row[1])
            counter += 1

def count(type, status):
    res = cur.execute(
        f'SELECT title, url, status FROM articles WHERE type is "{type}" and status is "{status}"')
    counter = 0
    for row in res.fetchall():
        counter += 1
    return counter


@bot.event
async def on_ready():
    print(f'{bot.user} succesfully logged in!')


@bot.command(name='follow', help='!follow type - start follow news type on private channel nick-type')
async def follow(ctx, arg):
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
                break
        await ctx.guild.create_text_channel(channel_name, overwrites=overwrites)
        await ctx.send('you start follow ' + arg + ' newses!')
        for channel in ctx.guild.channels:
            if channel.name == channel_name:
                new = count(str(arg), "New")
                update = count(str(arg), "Update")
                task_generator(channel, arg, new, update)
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
    res = cur.execute(f'SELECT url FROM sites WHERE url = "{site}"')
    url = res.fetchone()
    if url[0] == arg1:
        founded = True
    if arg2 == "sport" or arg2 == "moto" or arg2 == "biznes":
        if founded is True:
            await ctx.send(f'{site} already added!')
        elif re.match(url_pattern, site):
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
    res = cur.execute(f'SELECT url FROM sites WHERE url = "{site}"')
    url = res.fetchone()
    if url[0] == arg1:
        founded = True
    if founded is True:
        cur.execute(f'DELETE FROM sites WHERE url = "{site}"')
        con.commit()
        await ctx.send(f'You deleted {site} from database!')
    else:
        await ctx.send('This site is not in database!')

# ADVANCE SEARCH


@bot.command(name='search', help='!search text - you can search newest article having text in title.')
async def search(ctx, args):
    res = cur.execute("SELECT title, url, details FROM articles")
    founded = False
    param = ''
    for a in args:
        param += a + ' '
    param = param.lower()
    for row in reversed(res.fetchall()):
        title = str(row[0]).lower()
        url = str(row[1])
        details = str(row[2]).lower()
        matcher = SequenceMatcher(None, param, title).ratio()
        print(matcher)
        if title.find(param) != -1 or details.find(param) != -1 or matcher > 0.2:
            await ctx.send(title + " " + url)
            founded = True
            break
    if founded is False:
        await ctx.send("No articles!")


@bot.command(name='show_sites', help='!show_sites - you can check news sites.')
async def show_sites(ctx):
    msg = '```'
    res = cur.execute("SELECT url, type FROM sites")
    for url, type in res.fetchall():
        msg += url + " - " + type + "\n"
    msg += '```'
    await ctx.send(msg)


@bot.command(name='show_types', help='!show_types - you can check news types.')
async def show_types(ctx):
    msg = '```'
    res = cur.execute("SELECT type FROM sites GROUP BY type")
    for row in res.fetchall():
        msg += str(row[0]) + "\n"
    msg += '```'
    await ctx.send(msg)

bot.run(TOKEN)
