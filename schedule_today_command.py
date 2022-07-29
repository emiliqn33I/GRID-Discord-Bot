from formatting import format_timezone, format_allSeries_message
from execute_query import get_all_series_query

def schedule_today(message, endCursor):
  date = message.created_at
  data = get_all_series_query(date, "null", endCursor)
  
  if(data and "errors" not in data and len(data["data"]["allSeries"]["edges"]) != 0):
    format_timezone(data)
    return format_allSeries_message(data), data["data"]["allSeries"]["pageInfo"]["hasNextPage"], data["data"]["allSeries"]["pageInfo"]["endCursor"]
  else:
    return format_allSeries_message(data), None, None
