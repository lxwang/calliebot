from discord.ext import commands, tasks
import discord
import re
import json 
import time 
import random
import asyncio
import os
import datetime

# local import 
from tokens import dev, prod

message2 = 'strikes marked with * means good value'

client = commands.Bot(command_prefix='!')
@client.command()
async def test(ctx):
    await ctx.send('testing')
    pass

@client.event
async def on_ready():
    print(client.user.name)

@client.command()
async def calliebot(ctx, *arg): # <--- *arg stores arguments as tuples. Check print statements to see how it works
    with open('./callie_scripts/option_long_filter.json') as f:
        options_long_filtered = json.load(f) # this is a list

    with open('./callie_scripts/option_short_filter.json') as f:
        options_short_filtered = json.load(f) # this is a list

    with open('callie_scripts/scan_time.json') as f:
        scan_time_json = json.load(f) # this is a string

    #with open('date_range.json') as f: 
        #date_range_json = json.load(f)  # this is a list

    print('in calliebot')
    print(arg) # <--- tuple. access tuple like a list/array 

    if arg:
        roles = ctx.guild.roles # <--- get server roles
        author_role = ctx.author.roles # <-- all message author roles
        if arg[0] == '20':
            message = "calliebot 20"
            print('in 20 ')
            message = ""
            print(options_long_filtered)
            for company in options_long_filtered:
                message += f"{company['ticker']} / `{company['strikes']}` / {company['dates']}\n"
            #message_ = await ctx.send(f'`callies within 14 days | {message2} | scanned EST {scan_time_json} `')
            message_2 = await ctx.send(message)
            await asyncio.sleep(30)
            await ctx.message.delete()
            await discord.Message.delete(message_2)

        if arg[0] == '14':
            message = ""
            try:
                print('in try')
                print(arg[1])
                if arg[1].lower() == 'er':
                    print('in if')
                    for company in options_short_filtered:
                        message += f"{company['ticker']} / `{company['strikes']}` / {company['dates']}\n"
                        print(message)
                    #message_ = await ctx.send(f'`callies within 14 days | {message2} | scanned EST {scan_time_json} `')
                    message_2 = await ctx.send(message)
                    await asyncio.sleep(30)
                    await ctx.message.delete()
                    #await discord.Message.delete(message_)

            except:
                print('in except')
                message = ""
                for company in options_short_filtered:
                    print(company)
                    message += f"{company['ticker']} / `{company['strikes']}` / {company['dates']}\n "
                # message_ = await ctx.send(f'`callies within 14 days | {message2} | scanned EST {scan_time_json} `')
                message_2 = await ctx.send(message)
                await asyncio.sleep(30)
                await ctx.message.delete()
                await discord.Message.delete(message_2)
        else:
            pass

# async tasks
# prod
client.run(prod)
# dev
# client.run(dev)