from formatting import format_timezone, format_allSeries_message, format_concurrency_message
from execute_query import get_all_series_query, get_all_titles_query

def concurrency_title(message, endCursor):
  message_without_command = message.content.replace("concurrency", "")
  titleId = "null"
  validTitle = True
  
  titles_data = get_all_titles_query()
  for i in titles_data["data"]["titles"]:
    if(message_without_command == i["nameShortened"]):
      titleId = i["id"]
      break
  if(titleId == "null"):
    validTitle = False
    data = ""

  if(validTitle):
    date = message.created_at
    data = get_all_series_query(date, titleId, endCursor)
    if(data and "errors" not in data and len(data["data"]["allSeries"]["edges"]) != 0):
      return format_concurrency_message(data), data["data"]["allSeries"]["pageInfo"]["hasNextPage"], data["data"]["allSeries"]["pageInfo"]["endCursor"]
    else:
      return format_concurrency_message(data), None, None
  return format_concurrency_message(data), None, None