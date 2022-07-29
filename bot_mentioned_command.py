from formatting import format_prefixes

async def bot_mentioned(message, client, prefixes):
  try:
    if(message.mentions[0] == client.user):
      message.content = message.content.replace(client.user.mention, "")
      if(message.content == ""):
        await message.channel.send(embed=format_prefixes(client, message, prefixes))
        return False
      else:
        message.content = message.content[1:]
        return True
  except:
    pass