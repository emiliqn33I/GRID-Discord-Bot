import json
import os
import consts
from formatting import format_set_prefix, format_add_prefix, format_remove_prefix

def get_prefixes(client, message): # get prefixes for server
  with open(consts.server_prefixes_file, 'r') as f:
    prefixes = json.load(f)
  return prefixes[str(message.guild.id)] 

def set_prefixes_on_join(guild):
  if(not os.path.exists(consts.server_prefixes_file)):
      f = open(consts.server_prefixes_file, 'w+')
      f.write("{}")
      f.close()
  with open(consts.server_prefixes_file, 'r+') as f: # read the prefix.json file
    prefixes = json.load(f) # load the json file

  prefixes[str(guild.id)] = ['!'] # setting default prefix

  with open(consts.server_prefixes_file, 'w') as f: # save default prefix
    json.dump(prefixes, f, indent=2)

def set_prefixes_on_remove(guild):
  if(not os.path.exists(consts.server_prefixes_file)):
    return
  
  with open(consts.server_prefixes_file, 'r') as f: # read the file
    prefixes = json.load(f)

  prefixes.pop(str(guild.id)) # find the guild.id that bot was removed from

  with open(consts.server_prefixes_file, 'w') as f: # deletes the guild.id as well as its prefix
    json.dump(prefixes, f, indent=2)

def add_prefix(message):
  message.content = message.content.replace("prefixadd", "")
  with open(consts.server_prefixes_file, 'r') as f:
    prefixes = json.load(f)

  if(message.content not in prefixes[str(message.guild.id)]):
    prefixes[str(message.guild.id)].append(message.content)

    with open(consts.server_prefixes_file, 'w') as f: # saves the new dictionary of prefixes into the .json
      json.dump(prefixes, f, indent=2)

    embedVar = format_add_prefix(message.content, False)
  else:
    embedVar = format_add_prefix(message.content, True)

  return embedVar

def set_prefix(message):
  message.content = message.content.replace("prefixset", "")
  with open(consts.server_prefixes_file, 'r') as f:
    prefixes = json.load(f)

  prefixes[str(message.guild.id)] = [message.content]

  with open(consts.server_prefixes_file, 'w') as f: # saves the new dictionary of prefixes into the .json
    json.dump(prefixes, f, indent=2)

  embedVar = format_set_prefix(message.content)

  return embedVar

def remove_prefix(message):
  message.content = message.content.replace("prefixremove", "")
  with open(consts.server_prefixes_file, 'r') as f:
    prefixes = json.load(f)

  if(message.content in prefixes[str(message.guild.id)]):
    prefixes[str(message.guild.id)].remove(message.content)

    with open(consts.server_prefixes_file, 'w') as f: # saves the new dictionary of prefixes into the .json
      json.dump(prefixes, f, indent=2)

    embedVar = format_remove_prefix(message.content, True)
  else:
    embedVar = format_remove_prefix(message.content, False)
  
  
  return embedVar