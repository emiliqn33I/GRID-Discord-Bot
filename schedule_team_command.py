from execute_query import get_all_series_query

def compare_teams(team1, team2):
  if((team1.casefold() in team2.casefold()) or 
     (team2.casefold() in team1.casefold())):
       return True
  
  return False

def find_teams(team1):
  for node in schedule_team.data["data"]["allSeries"]["edges"]:
    for team in node["node"]["teams"]:
      team2 = team["baseInfo"]["name"]
      if(compare_teams(team1, team2)):
        schedule_team.similarTeams.add(team2)

def schedule_team(message, endCursor):
  message.content = message.content.replace("scheduleteam", "")
  if(message.content == ""):
    return None, None
  
  date = message.created_at
  if(len(schedule_team.data) == 0):
    schedule_team.data = get_all_series_query(date, "null", endCursor)

    if(schedule_team.data and "errors" not in schedule_team.data and len(schedule_team.data["data"]["allSeries"]["edges"]) != 0):
      pass
    else:
      return None, None
    
    find_teams(message.content)
    return schedule_team.data["data"]["allSeries"]["pageInfo"]["hasNextPage"], schedule_team.data["data"]["allSeries"]["pageInfo"]["endCursor"]
  else:
    data = get_all_series_query(date, "null", endCursor)
    if(data and "errors" not in data and len(data["data"]["allSeries"]["edges"]) != 0):
      pass
    else:
      return None, None 
    for node in data["data"]["allSeries"]["edges"]:
      schedule_team.data["data"]["allSeries"]["edges"].append(node)
    find_teams(message.content)

    return data["data"]["allSeries"]["pageInfo"]["hasNextPage"], data["data"]["allSeries"]["pageInfo"]["endCursor"]