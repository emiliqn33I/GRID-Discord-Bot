from formatting import format_allSeries_message, format_tournament_series_message, format_timezone, format_concurrency_message
from schedule_today_command import schedule_today
from schedule_date_command import schedule_date
from schedule_title_command import schedule_title
from schedule_team_command import schedule_team
from schedule_tournament_command import schedule_tournament
from tournament_seriesid_command import tournament_seriesid
from concurrency_title_command import concurrency_title

import discord

def pagination(message, command):  
  endCursor = "null"
  hasNextPage = True
  allPages = []
  format_allSeries_message.counter = 1
  format_tournament_series_message.counter = 1

  schedule_team.similarTeams = set()
  schedule_team.options = list()
  schedule_team.data = dict()
  schedule_team.counter = 1

  schedule_tournament.similarTournaments = set()
  schedule_tournament.options = list()
  schedule_tournament.data = dict()
  schedule_tournament.counter = 1

  format_concurrency_message.count_bo1 = 0
  format_concurrency_message.count_bo2 = 0
  format_concurrency_message.count_bo3 = 0
  format_concurrency_message.count_bo4 = 0
  format_concurrency_message.count_bo5 = 0
  format_concurrency_message.dict_pair = dict()
  #format_concurrency_message.dict_pair.clear()
  
  while(hasNextPage):
    if(command == "scheduletoday"):
      embedVar, hasNextPage, endCursor = schedule_today(message, endCursor)
    elif(command.startswith("scheduledate")):
      embedVar, hasNextPage, endCursor = schedule_date(message, endCursor)
    elif(command.startswith("scheduletitle")):
      embedVar, hasNextPage, endCursor = schedule_title(message, endCursor)
    elif(command.startswith("concurrency")):
      embedVar, hasNextPage, endCursor = concurrency_title(message, endCursor)
      allPages = None
    elif(command.startswith("scheduleteam")):
      hasNextPage, endCursor = schedule_team(message, endCursor)
      allPages = None
      embedVar = None
      if(hasNextPage == None or endCursor == None):
        return None, format_allSeries_message(None)
    elif(command.startswith("scheduletournament")):
      hasNextPage, endCursor = schedule_tournament(message, endCursor)
      allPages = None
      embedVar = None
      if(hasNextPage == None or endCursor == None):
        return None, format_allSeries_message(None)
    elif(command.startswith("tournament")):
      embedVar, hasNextPage, endCursor = tournament_seriesid(message, endCursor)

    if(hasNextPage == None or endCursor == None):
      return None, embedVar
    if(not command.startswith("scheduleteam") and not command.startswith("scheduletournament") and not command.startswith("concurrency")):
      allPages.append(embedVar)

  if(command.startswith("scheduleteam")):
      format_timezone(schedule_team.data)
      for i in schedule_team.similarTeams:
        schedule_team.options.append(discord.SelectOption(label = str(schedule_team.counter) + " - " + i, emoji = "➡️"))
        schedule_team.counter += 1
  elif(command.startswith("scheduletournament")):
      format_timezone(schedule_tournament.data)
      for i in schedule_tournament.similarTournaments:
        schedule_tournament.options.append(discord.SelectOption(label = str(schedule_tournament.counter) + " - " + i, emoji = "➡️"))
        schedule_tournament.counter += 1

  return allPages, embedVar