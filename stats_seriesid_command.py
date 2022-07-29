from formatting import format_invalid_seriesid, format_liveSeries_message, format_liveSeries_no_result
from execute_query import get_live_series_query, get_live_series_query_all_games
import copy

def stats_seriesid(message):
  message.content = message.content.replace("stats", "")
  if(message.content.isnumeric()):
    # Finished games
    data = get_live_series_query(message.content, "finished")
    finished_games = 0
    for i in data["data"]["seriesState"]["games"]:
      if i["sequenceNumber"] != None:
        finished_games = i["sequenceNumber"]

    # Started games
    data = get_live_series_query(message.content, "started")
    started_games_data = copy.deepcopy(data)

    # Team wins
    data = get_live_series_query(message.content, "finished")
    counter_team1_wins = 0
    counter_team2_wins = 0

    teams = []
    if(data["data"] == None):
      return format_liveSeries_no_result()
    for i in data["data"]["seriesState"]["teams"]:
      teams.append(i["name"])

    for i in data["data"]["seriesState"]["games"]:
      for j in i["teams"]:
        if i:
          if j["name"] == teams[0]:
            if j["won"]:
              counter_team1_wins += 1
          if j["name"] == teams[1]:
            if j["won"]:
              counter_team2_wins += 1

    arr_of_team_wins = [counter_team1_wins, counter_team2_wins]

    # All games
    data = get_live_series_query_all_games(message.content) 

    return format_liveSeries_message(started_games_data, finished_games, arr_of_team_wins, data)
  else:
    return format_invalid_seriesid(message.content)