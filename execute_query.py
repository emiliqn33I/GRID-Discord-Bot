import requests
from datetime import timedelta

import consts

def get_all_series_query(date, titleId, endCursor):
  #timezone = date.astimezone() # converts date to local timezone, could be kept as UTC in line below
  timezone = date
  timezone = timezone.replace(hour=0, minute=0, second=0, microsecond=0) # moves time to the start of the day
  
  quotes = "\""
  if(endCursor == "null"):
    quotes = ""
  
  # .isoformat() - formats date into ISO 8601 format and turns it into a string type
  # timedelta() - used to add 24 hours (1 day) to the current time
  query = f"""
  {{
    allSeries (
      filter:{{
        startTimeScheduled:{{
          gte: \"""" + timezone.isoformat() + "\"" + """ 
          lte: \"""" + (timezone + timedelta(days=1)).isoformat() + "\"" + """
        }
        titleId: """ + titleId + """
      }
      after: """ + quotes + endCursor + quotes + """
      orderBy: StartTimeScheduled
    ) {
      totalCount,
      pageInfo{
        hasPreviousPage
        hasNextPage
        startCursor
        endCursor
      }
      edges {
        node {
          id
          format {
            name
            nameShortened
          }
          startTimeScheduled
          title {
            name
            nameShortened
          }
          tournament {
            name
          }
          teams {
            baseInfo {
              name
            }
          }
        }
      }
    }
  }
  """

  url = "https://api-op.grid.gg/central-data/graphql"
  r = requests.post(url, headers=consts.headers, json={"query": query})
  data = r.json()

  return data

def get_all_titles_query():
  query = f"""
  {{
    titles {{
      id
      name
      nameShortened
    }}
  }}
"""

  url = "https://api-op.grid.gg/central-data/graphql"
  r = requests.post(url, headers=consts.headers, json={"query": query})
  data = r.json()

  return data

def get_live_series_query_all_games(seriesId):
  query = f"""
  {{
    seriesState(id: \"""" + seriesId + "\"" + """) {   
      games {
        map {
          name
        }
        teams {
          name
          netWorth
          kills
          deaths
          players {
            name
            kills
            killAssistsGiven
            deaths
            netWorth
          }
          }
        }
      }
  }"""

  url = "https://api-op.grid.gg/live-data-feed/series-state/graphql"
  r = requests.post(url, headers=consts.headers, json={"query": query})
  data = r.json()

  return data

def get_live_series_query(seriesId, started_or_finished):
  query = f"""
  {{
    seriesState(id:  \"""" + seriesId + "\"" + """) {
      format
      teams {
        name
      }
      games(filter: { """ + started_or_finished + """: true }) {
        sequenceNumber
        teams {
          name
          won
          players {
            name
          }
        }
      }
    }
  }
  """

  url = "https://api-op.grid.gg/live-data-feed/series-state/graphql"
  r = requests.post(url, headers=consts.headers, json={"query": query})
  data = r.json()

  return data

def get_tournament_series_query(tournamentId, endCursor):

  quotes = "\""
  if(endCursor == "null"):
    quotes = ""

  query = f"""
  {{
    allSeries (
      filter: {{
        tournamentId: """ + tournamentId + """
      }, 
        first: 5
        after: """ + quotes + endCursor + quotes + """
        orderBy: StartTimeScheduled
    ) {
      totalCount
      pageInfo {
        hasPreviousPage
        hasNextPage
        startCursor
        endCursor
      }
      edges {
        node {
          id
          title {
            name
          }
          tournament {
            nameShortened
          }
          startTimeScheduled
          format {
            name
          }
          teams {
            baseInfo {
              name
            }
          }
        }
      }
    }
  }
  """

  url = "https://api-op.grid.gg/central-data/graphql"
  r = requests.post(url, headers=consts.headers, json={"query": query})
  data = r.json()

  return data