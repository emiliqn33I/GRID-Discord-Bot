from execute_query import get_all_series_query

def compare_tournaments(tournament1, tournament2):
  if((tournament1.casefold() in tournament2.casefold()) or 
     (tournament2.casefold() in tournament1.casefold())):
       return True
  
  return False

def find_tournaments(tournament1):
  for node in schedule_tournament.data["data"]["allSeries"]["edges"]:
    tournament2 = node["node"]["tournament"]["name"]
    if(compare_tournaments(tournament1, tournament2)):
      schedule_tournament.similarTournaments.add(tournament2)
        
  return schedule_tournament.similarTournaments

def schedule_tournament(message, endCursor):
  message.content = message.content.replace("scheduletournament", "")
  if(message.content == ""):
    return None, None
  
  date = message.created_at
  if(len(schedule_tournament.data) == 0):
    schedule_tournament.data = get_all_series_query(date, "null", endCursor)

    if(schedule_tournament.data and "errors" not in schedule_tournament.data and len(schedule_tournament.data["data"]["allSeries"]["edges"]) != 0):
      pass
    else:
      return None, None
    
    find_tournaments(message.content)
    return schedule_tournament.data["data"]["allSeries"]["pageInfo"]["hasNextPage"], schedule_tournament.data["data"]["allSeries"]["pageInfo"]["endCursor"]
  else:
    data = get_all_series_query(date, "null", endCursor)
    if(data and "errors" not in data and len(data["data"]["allSeries"]["edges"]) != 0):
      pass
    else:
      return None, None 
    for node in data["data"]["allSeries"]["edges"]:
      schedule_tournament.data["data"]["allSeries"]["edges"].append(node)
    find_tournaments(message.content)

    return data["data"]["allSeries"]["pageInfo"]["hasNextPage"], data["data"]["allSeries"]["pageInfo"]["endCursor"]