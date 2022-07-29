import discord
from discord.ext import commands

from help_command import help
from ping_command import ping
from invalid_command import invalid_command
from schedule_team_command import schedule_team
from schedule_tournament_command import schedule_tournament
from stats_seriesid_command import stats_seriesid
from formatting import format_allSeries_message, concurrency_format_embed_field, format_team, format_tournament, format_prefixes, format_similar_teams, \
format_message, format_loading, format_too_many_team_results_message, format_too_many_tournament_results_message
from prefixes import set_prefixes_on_join, set_prefixes_on_remove, get_prefixes, set_prefix, add_prefix, remove_prefix
import consts
import config
from bot_mentioned_command import bot_mentioned
from button import ButtonView, create_initial_buttons
from select_menu import SelectView
from pagination import pagination

intents = discord.Intents.default()
intents.message_content = True

client=commands.Bot(command_prefix=commands.when_mentioned_or(get_prefixes), intents=intents)
client.remove_command('help')

@client.event
async def on_ready():
  print('Bot {0.user}'.format(client) + ' has started')

@client.event
async def on_guild_join(guild):
  set_prefixes_on_join(guild)

@client.event
async def on_guild_remove(guild):
  set_prefixes_on_remove(guild)

@client.event
async def on_message(message):
  if(message.author == client.user):
    return
  
  botHasBeenMentionedWithCommand = await bot_mentioned(message, client, get_prefixes(client, message))

  if(botHasBeenMentionedWithCommand or message.content.startswith(tuple(get_prefixes(client, message)))):
    used_prefix = format_message(message, get_prefixes(client, message), botHasBeenMentionedWithCommand)

    if(message.content == ('help')):
      await message.channel.send(embed=(help(used_prefix))[0], view=ButtonView(create_initial_buttons((help(used_prefix)), message.author), message.author))
    elif(message.content == ('ping')):
      await message.channel.send(embed = ping(round(client.latency * 1000)))
    elif(message.content == ('prefix')):
      await message.channel.send(embed=format_prefixes(client, message, get_prefixes(client, message)))
    elif(message.content.startswith('prefixadd')):
      await message.channel.send(embed=add_prefix(message))
    elif(message.content.startswith('prefixset')):
      await message.channel.send(embed=set_prefix(message))
    elif(message.content.startswith('prefixremove')):
      await message.channel.send(embed=remove_prefix(message))
    elif(message.content.startswith('stats')):
      await message.channel.send(embed=stats_seriesid(message))

    elif(message.content == ('scheduletoday') or message.content.startswith('scheduletitle') or  
         message.content.startswith('scheduledate') or message.content.startswith('tournament') or message.content.startswith('concurrency')):
      msg = await message.channel.send(embed=format_loading())
      allPages, embedVar = pagination(message, message.content)

      if(message.content.startswith('concurrency')):
        await msg.edit(embed=concurrency_format_embed_field(embedVar))
      else:
        if(allPages == None or len(allPages) == 0):
          await msg.edit(embed=embedVar)
        else:
          await msg.edit(embed=allPages[0], view=ButtonView(create_initial_buttons(allPages, message.author), message.author))
    elif(message.content.startswith('scheduleteam')):
      msg = await message.channel.send(embed=format_loading())
      pagination(message, message.content)

      if(len(schedule_team.similarTeams) == 0 or len(schedule_team.options) == 0):
        await msg.edit(embed=format_allSeries_message(""))
      elif(len(schedule_team.similarTeams) == 1):
        allPages = format_team(schedule_team.data, list(schedule_team.similarTeams)[0])
        await msg.edit(embed=allPages[0], view=ButtonView(create_initial_buttons(allPages, message.author), message.author))
      elif(len(schedule_team.options) > 25):
        await msg.edit(embed=format_too_many_team_results_message())
      else:
        embedVar = discord.Embed(title="Choose which teams you want to see the schedule for!", description = format_similar_teams(schedule_team.similarTeams), color=consts.purple)
        await message.channel.send(embed=embedVar, view=SelectView(schedule_team.options, schedule_team.data, "team", message.author))
    elif(message.content.startswith('scheduletournament')):
      msg = await message.channel.send(embed=format_loading())
      pagination(message, message.content)

      if(len(schedule_tournament.similarTournaments) == 0 or len(schedule_tournament.options) == 0):
        await msg.edit(embed=format_allSeries_message(""))
      elif(len(schedule_tournament.similarTournaments) == 1):
        allPages = format_tournament(schedule_tournament.data, list(schedule_tournament.similarTournaments)[0])
        await msg.edit(embed=allPages[0], view=ButtonView(create_initial_buttons(allPages, message.author), message.author))
      elif(len(schedule_tournament.options) > 25):
        await msg.edit(embed=format_too_many_tournament_results_message())
      else:
        embedVar = discord.Embed(title="Choose which tournaments you want to see the schedule for!", description = format_similar_teams(schedule_tournament.similarTournaments), color=consts.purple)
        await message.channel.send(embed=embedVar, view=SelectView(schedule_tournament.options, schedule_tournament.data, "tournament", message.author))

    else:
      await message.channel.send(embed=(invalid_command(used_prefix))[0], view=ButtonView(create_initial_buttons((invalid_command(used_prefix)), message.author), message.author))

client.run(config.TOKEN)
