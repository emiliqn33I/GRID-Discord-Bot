from formatting import format_tournament_series_message
from execute_query import get_tournament_series_query

def tournament_seriesid(message, endCursor):
  message.content = message.content.replace("tournament", "")

  data = get_tournament_series_query(message.content, endCursor)

  if(data and "errors" not in data and len(data["data"]["allSeries"]["edges"]) != 0):
    return format_tournament_series_message(data), data["data"]["allSeries"]["pageInfo"]["hasNextPage"], data["data"]["allSeries"]["pageInfo"]["endCursor"]
  else:
    return format_tournament_series_message(data), None, None