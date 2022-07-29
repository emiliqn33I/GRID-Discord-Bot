from formatting import format_timezone, format_allSeries_message, format_invalid_date
from execute_query import get_all_series_query
from datetime import datetime

def schedule_date(message, endCursor):
  message.content = message.content.replace("scheduledate", "")
  try:
    date = datetime.strptime(message.content, '%Y-%m-%d')
  except:
    return format_invalid_date(), None, None
  data = get_all_series_query(date, "null", endCursor)
  
  if(data and "errors" not in data and len(data["data"]["allSeries"]["edges"]) != 0):
    format_timezone(data)
    return format_allSeries_message(data), data["data"]["allSeries"]["pageInfo"]["hasNextPage"], data["data"]["allSeries"]["pageInfo"]["endCursor"]
  else:
    return format_allSeries_message(data), None, None
