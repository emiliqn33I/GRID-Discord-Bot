from datetime import datetime
import calendar
import discord
import consts
import copy
from collections import Counter

def format_message(message, prefixes, botHasBeenMentionedWithCommand):
  message.content = message.content.replace(" ", "")
  message.content = message.content.casefold()

  used_prefix = ""
  if(not botHasBeenMentionedWithCommand):
    for i in prefixes:
      used_prefix = message.content[:(len(i))]
      if (i == used_prefix):
        message.content = message.content.replace(i, "", 1)
        break
  
  return used_prefix

def format_loading():
  return discord.Embed(title=":arrows_clockwise: Loading results... :arrows_clockwise:", description = ":hourglass: Please wait! :hourglass:", color=consts.purple)

def format_help(prefix):
  allPages = []
  embedVar = discord.Embed(title=":book: Esports Bot Commands", color=consts.purple)
  commands = ""

  for i in range(len(consts.commands)):
    if(i % 5 == 0 and i != 0):
      embedVar.description = commands
      allPages.append(embedVar)
      commands = ""
      embedVar = discord.Embed(title=":book: Esports Bot Commands", color=consts.purple)

    commands += consts.commands[i] + '\n\n'

  embedVar.description = commands
  allPages.append(embedVar)

  if(prefix == ""):
    reset_commands()

  return allPages

def format_invalid_command(prefix):
  allPages = []
  embedVar = discord.Embed(title=":x: Invalid Command!", color=consts.purple)
  commands = ""

  for i in range(len(consts.commands)):
    if(i % 5 == 0 and i != 0):
      embedVar.description = commands
      allPages.append(embedVar)
      commands = ""
      embedVar = discord.Embed(title=":x: Invalid Command!", color=consts.purple)

    commands += consts.commands[i] + '\n\n'

  embedVar.description = commands
  allPages.append(embedVar)

  if(prefix == ""):
    reset_commands()

  return allPages

def reset_commands():
  for i in range(0, len(consts.commands)):
    str = consts.commands[i]
    consts.commands[i] = str[:3] + "!" + str[3:]

def format_ping(ping):
  return discord.Embed(title=(":ping_pong: Pong!"), description=("**" + str(ping) + " ms**"), color=consts.purple)

def format_prefixes(client, message, prefixes):
  output = [("1. " + str(client.user.mention))]
  for i in range(len(prefixes)):
    output.append(str(i + 2) + ". **" + prefixes[i] + "**")
  output = '\n'.join(output)
  return discord.Embed(title=("Prefixes"), description=output, color=consts.purple)

def format_add_prefix(prefix, prefixExists):
  if(not prefixExists):
    return discord.Embed(title=("New prefix **" + prefix + "** has been added successfully!"), color=consts.purple)
  else:
    return discord.Embed(title=(":x: Prefix already exists!"), color=consts.purple)

def format_set_prefix(prefix):
  return discord.Embed(title=("Prefix now set to: **" + prefix + "**"), color=consts.purple)

def format_remove_prefix(prefix, prefixFound):
  if(prefixFound):
    return discord.Embed(title=("Prefix **" + prefix + "** has been removed successfully!"), color=consts.purple)
  else:
    return discord.Embed(title=(":x: I do not have this prefix registered."), color=consts.purple)

def format_timezone(data):
  for node in data["data"]["allSeries"]["edges"]:
    # datetime.strptime - string to datetime
    # .utctimetuple() - converts datetime to a UTC time tuple object a.k.a time.struct_time. Helps in converting datetime to a UNIX timestamp
    # calendar.timegm() - converts from a UTC timestamp to a UNIX timestamp
    node["node"]["startTimeScheduled"] = "<t:" + str(calendar.timegm((datetime.strptime(node["node"]["startTimeScheduled"], '%Y-%m-%dT%H:%M:%S%z')).utctimetuple())) + ":F>"

def format_invalid_date():
  return discord.Embed(title=(":x: Invalid date given!"), description="Make sure date format is {yyyy-mm-dd} !", color=consts.purple)

def format_team(data, chosenTeam):
  data_copy = copy.deepcopy(data)
  for i in range(len(data_copy["data"]["allSeries"]["edges"]) - 1, -1, -1):
    if (data_copy["data"]["allSeries"]["edges"][i]["node"]["teams"][0]["baseInfo"]["name"] != chosenTeam and 
        data_copy["data"]["allSeries"]["edges"][i]["node"]["teams"][1]["baseInfo"]["name"] != chosenTeam):
      del data_copy["data"]["allSeries"]["edges"][i]
  
  format_team_message.counter = 1
  return format_team_message(data_copy)

def format_team_message(data):
  embedVar = discord.Embed(title=":calendar: Today's Tournament Schedule", description = "Displays today's ongoing tournaments.", color=consts.purple)
  allPages = []
  
  for i in data["data"]["allSeries"]["edges"]:
    embedVar.add_field(name=("{} {}".format("**Tournament", str(format_team_message.counter) + " **\n")), value=
      (":id: Series Id: " + i["node"]["id"] + "\n"
      + ":clock10: Start Time: "+ i["node"]["startTimeScheduled"] + "\n"
      ":handshake: Teams: " + i["node"]["teams"][0]["baseInfo"]["name"] + " VS " + i["node"]["teams"][1]["baseInfo"]["name"] + "\n"
      + ":video_game: Title: " + i["node"]["title"]["name"] + "\n"
      + ":trophy: Tournament: " + i["node"]["tournament"]["name"] + "\n\n"), inline=False)
    format_team_message.counter += 1

    if(format_team_message.counter % 5 == 0):
      format_team_message.counter = 1
      allPages.append(embedVar)
      embedVar = discord.Embed(title=":calendar: Today's Tournament Schedule", description = "Displays today's ongoing tournaments.", color=consts.purple)

  allPages.append(embedVar)
  return allPages

def format_tournament(data, chosenTournament):
  data_copy = copy.deepcopy(data)

  for i in range(len(data_copy["data"]["allSeries"]["edges"]) - 1, -1, -1):
    if (data_copy["data"]["allSeries"]["edges"][i]["node"]["tournament"]["name"] != chosenTournament):
        del data_copy["data"]["allSeries"]["edges"][i]

  format_tournament_message.counter = 1
  return format_tournament_message(data_copy)

def format_tournament_message(data):
  embedVar = discord.Embed(title=":calendar: Today's Tournament Schedule", description = "Displays today's ongoing tournaments.", color=consts.purple)
  allPages = []
  
  for i in data["data"]["allSeries"]["edges"]:
    embedVar.add_field(name=("{} {}".format("**Tournament", str(format_tournament_message.counter) + " **\n")), value=
      (":id: Series Id: " + i["node"]["id"] + "\n"
      + ":clock10: Start Time: "+ i["node"]["startTimeScheduled"] + "\n"
      ":handshake: Teams: " + i["node"]["teams"][0]["baseInfo"]["name"] + " VS " + i["node"]["teams"][1]["baseInfo"]["name"] + "\n"
      + ":video_game: Title: " + i["node"]["title"]["name"] + "\n"
      + ":trophy: Tournament: " + i["node"]["tournament"]["name"] + "\n\n"), inline=False)
    format_tournament_message.counter += 1

    if(format_tournament_message.counter % 5 == 0):
      allPages.append(embedVar)
      embedVar = discord.Embed(title=":calendar: Today's Tournament Schedule", description = "Displays today's ongoing tournaments.", color=consts.purple)

  allPages.append(embedVar)
  return allPages

def format_similar_teams(similarTeams):
  presentTeams = ""
  counter = 1
  for i in similarTeams:
    presentTeams += str(counter) + " - " + i + '\n'
    counter += 1
  
  return presentTeams

def format_allSeries_message(data):
  if(data == None or "errors" in data or data == "" or len(data["data"]["allSeries"]["edges"]) == 0):
    embedVar = discord.Embed(title=":calendar: Today's Tournament Schedule", description = "Displays today's ongoing tournaments.", color=consts.purple)
    embedVar.add_field(name="No results found!", value = "⠀", inline=False)
  else:
    embedVar = discord.Embed(title=":calendar: Today's Tournament Schedule", description = "Displays today's ongoing tournaments.", color=consts.purple)
    
    for i in data["data"]["allSeries"]["edges"]:
      teams = []
  
      for j in i["node"]["teams"]:
        teams.append(j["baseInfo"]["name"])
      
      s = teams[0] + " VS " + teams[1]
      embedVar.add_field(name=("{} {}".format("**Tournament", str(format_allSeries_message.counter) + " **\n")), value=
        (":id: Series Id: " + i["node"]["id"] + "\n"
        + ":clock10: Start Time: "+ i["node"]["startTimeScheduled"] + "\n"
        ":handshake: Teams: " + s + "\n"
        + ":video_game: Title: " + i["node"]["title"]["name"] + "\n"
        + ":trophy: Tournament: " + i["node"]["tournament"]["name"] + "\n\n"), inline=False)
      format_allSeries_message.counter += 1
  return embedVar 

def format_liveSeries_message(data, num_finished_games, list_wins, data_all_games):
  if(data == None or "errors" in data or data == "" or len(data["data"]["seriesState"]) == 0):
    embedVar = discord.Embed(title=":calendar: Today's Tournament Schedule", description = "Displays today's ongoing tournaments.", color=consts.purple)
    embedVar.add_field(name="No results found!", value = "⠀", inline=False)
  else:
    teams = []
    for i in data["data"]["seriesState"]["teams"]:
      teams.append(i["name"])
      
    embedVar = discord.Embed(title=":chart_with_upwards_trend: **In Game Stats **\n", description = 
          (":newspaper: **Format**: " + data["data"]["seriesState"]["format"].replace("-", " ").capitalize() + "\n"
          + ":vs: **Teams**: " + teams[0].replace("-", " ")+" VS " + teams[1].replace("-", " ")+"\n"
          + ":video_game: **Games played**: {}".format(num_finished_games) + "\n"
          + ":trophy: **Wins for team** " + teams[0].replace("-", " ")+": " + "{}".format(list_wins[0])+"\n"
          + ":trophy: **Wins for team** " + teams[1].replace("-", " ")+": " + "{}".format(list_wins[1])+"\n"
        ), color=0x370F65)

    counter_game = 1
    counter_team_map = 0
    maps = []
      
    if data_all_games["data"]["seriesState"]["games"]:
      for i in data_all_games["data"]["seriesState"]["games"]:
        teams = []
        networth = []
        kills = []
        deaths = []
        players_names = []
        networth_player = []
        player_kills = []
        player_assists = []
        player_deaths = []
        
        maps.append(i["map"]["name"])
        
        for j in i["teams"]:
          teams.append(j["name"])
          networth.append(j["netWorth"])
          kills.append(j["kills"])
          deaths.append(j["deaths"])

        for j in i["teams"]:
          for m in j["players"]:
            players_names.append(m["name"])
            networth_player.append(m["netWorth"])
            player_deaths.append(m["deaths"])
            player_kills.append(m["kills"])
            player_assists.append(m["killAssistsGiven"])
          
        embedVar.add_field(name=("**Game {}**".format(counter_game)+ "\n"), 
        value=(":map: **Map name:** " + maps[counter_team_map].capitalize() + "\n"+
                ":moneybag: **" + teams[0] + " Networth**" + ": {}".format(networth[0])+ "\n"
                ":knife: **" + teams[0] + " Kills:**" " {}".format(kills[0])+ "\n"
                ":skull: **" + teams[0] + " Deaths:**" + " {}".format(deaths[0])+ "\n"
                ":moneybag: **" + teams[1] + " Networth:**" + " {}".format(networth[1])+ "\n"
                ":knife: **" + teams[1] + " Kills:**" " {}".format(kills[1])+ "\n"
                ":skull: **" + teams[1] + " Deaths:**" + " {}".format(deaths[1])+ "\n"
                ":scales: **" + " Networth difference:** {}".format( abs(networth[1] - networth[0]) )+ "\n"
            ), inline=False)
        for k  in range(len(players_names)):
          embedVar.add_field(name=("⠀"), 
          value=(":video_game: **Player name: **" + players_names[k] +" \n"+
                ":money_with_wings: **Player networth:** {}".format(networth_player[k]) +" \n"+
                ":joystick: **Player K/D/A:** {}/{}/{}".format(player_kills[k], player_deaths[k], player_assists[k]) +" \n"), inline=False)

        counter_game += 1
        counter_team_map += 1
 
  return embedVar

def format_tournament_series_message(data):
  if(data == None or "errors" in data or data == "" or len(data["data"]["allSeries"]["edges"]) == 0):
    embedVar = discord.Embed(title=":x: **Tournament Id Not Found!**\n", description = "Displays all series for the given tournament.", color=consts.purple)
    embedVar.add_field(name="No results found!", value = "⠀", inline=False)
  else:
    embedVar = discord.Embed(title=":trophy: **Tournament: " + data["data"]["allSeries"]["edges"][0]["node"]["tournament"]["nameShortened"] + "**\n", description = ("Displays all series for the given tournament."), color=0x370F65)

    for j in data["data"]["allSeries"]["edges"]:
      embedVar.add_field(name=("{} {}".format("**Series", str(format_tournament_series_message.counter) + " **\n")),
                        value=(":newspaper: **Format: **" + j["node"]["format"]["name"].replace("-", " ").capitalize() + "\n" +
                                ":video_game: **Title: **" + j["node"]["title"]["name"] + "\n" +
                                ":clock10: **Start time:** " + j["node"]["startTimeScheduled"] + " \n" +
                                ":joystick: **Teams:** " + j["node"]["teams"][0]["baseInfo"]["name"] +" VS " + j["node"]["teams"][1]["baseInfo"]["name"] + "\n"), inline=False)
      format_tournament_series_message.counter += 1
   
  return embedVar

def format_concurrency_message(data):
  if(data == None or "errors" in data or data == "" or len(data["data"]["allSeries"]["edges"]) == 0):
    embedVar = discord.Embed(title=":x: Invalid title given!", description = "Displays today's title concurrency.", color=consts.purple)
    embedVar.add_field(name="No results found!", value = "⠀", inline=False)
  else:
    title = ""
    
    for i in data["data"]["allSeries"]["edges"]:
      title = i["node"]["title"]["nameShortened"]
      
    embedVar = discord.Embed(title=":trophy: **Title: "+ title.upper() +"**\n", color=0x370F65)

    for j in data["data"]["allSeries"]["edges"]:
      teams = []
      format_game = j["node"]["format"]["nameShortened"]

      if format_concurrency_message.dict_pair.get(format_game) != None:
        for k in range(int(j["node"]["startTimeScheduled"][11:13]), int(j["node"]["startTimeScheduled"][11:13])+int(format_game[2])):
          format_concurrency_message.dict_pair[format_game].append(k)
      else:
        format_concurrency_message.dict_pair[format_game] = ([])
        for k in range(int(j["node"]["startTimeScheduled"][11:13]), int(j["node"]["startTimeScheduled"][11:13])+int(format_game[2])):
          format_concurrency_message.dict_pair[format_game].append(k)
      
      if format_game.lower() == "bo1":
          format_concurrency_message.count_bo1 += 1
      if format_game.lower() == "bo2":
          format_concurrency_message.count_bo2 += 1
      if format_game.lower() == "bo3":
          format_concurrency_message.count_bo3 += 1
      if format_game.lower() == "bo5":
          format_concurrency_message.count_bo5 += 1
      
      for i in j["node"]["teams"]:
          teams.append(i["baseInfo"]["name"])

    sttring = ""
    if(format_concurrency_message.count_bo1 != 0):
      sttring += "  ✧ **Best of one:** {}".format(format_concurrency_message.count_bo1)+" series \n"
    if(format_concurrency_message.count_bo2 != 0):
      sttring += "  ✧ **Best of two:** {}".format(format_concurrency_message.count_bo2)+" series\n"
    if(format_concurrency_message.count_bo3 != 0):
      sttring += "  ✧ **Best of three: **{}".format(format_concurrency_message.count_bo3)+" series\n"
    if(format_concurrency_message.count_bo5 != 0):
      sttring += "  ✧ **Best of five: **{}".format(format_concurrency_message.count_bo5)+" series\n"

    embedVar.add_field(name=("There will be {}".format(format_concurrency_message.count_bo1 + 
                                                      format_concurrency_message.count_bo2 + 
                                                      format_concurrency_message.count_bo3 + 
                                                      format_concurrency_message.count_bo5) + 
                                                      " series for "+ title.upper() +" today" ),
                                                      value=sttring, inline=False)
  
  return embedVar

def concurrency_format_embed_field(embedVar):
  if(embedVar.title.startswith(":x:")):
    return embedVar
  
  l = []

  for i in format_concurrency_message.dict_pair.values():
    l.append(i)
  flatten_list = [j for sub in l for j in sub]
  most_repetitions_hour = str( (Counter(flatten_list).most_common(1))[0][0] )
  repetitions_of_format = {}
  string = ""

  for i in format_concurrency_message.dict_pair:
    if int(most_repetitions_hour) in format_concurrency_message.dict_pair[i]:
      repetitions_of_format[i] = (format_concurrency_message.dict_pair[i].count(int(most_repetitions_hour)))
      string += str(repetitions_of_format[i]) +" "+ i.replace("1", "one").replace("2", "two").replace("3", "three").replace("5", "five") + " and "

  string = string.replace("Bo", "best of ")
  string = string[:-5:]
  
  embedVar.add_field(name=("The highest concurrency today will be at " + most_repetitions_hour +
                          ":00, with "  + string + " being played at the same time"), value=("⠀"), inline=False)
  
  return embedVar

def format_liveSeries_no_result():
    embedVar = discord.Embed(title=":chart_with_upwards_trend: In Game Stats", color=consts.purple)
    embedVar.add_field(name="No results found!", value = "⠀", inline=False)
    return embedVar

def format_invalid_seriesid(message):
  return discord.Embed(title=(":x: **The Series Id \'" + message + "\' doesn't exist**\n"), color=consts.purple)

def format_too_many_team_results_message(): 
  return discord.Embed(title="**:x: Please send a more specific team name!**", description="**We found too many results for the team you're searching for!**", color=consts.purple)

def format_too_many_tournament_results_message(): 
  return discord.Embed(title="**:x: Please send a more specific tournament name!**", description="**We found too many results for the tournament you're searching for!**", color=consts.purple)
