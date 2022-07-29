import discord
from formatting import format_team, format_tournament
from button import ButtonView, create_initial_buttons

class Select(discord.ui.Select):
  def __init__(self, options, data, team_or_tournament_called, author):
    try:
      super().__init__(placeholder="Select an option",max_values=1,min_values=1,options=options)
      self.data = data
      self.team_or_tournament_called = team_or_tournament_called
      self.author = author
    except Exception as e:
      print(e)
  async def callback(self, interaction: discord.Interaction):
    string = self.values[0][4:]
    string = string.strip()
    
    if(self.team_or_tournament_called == "team"):
      allPages = format_team(self.data, string)
    else:
      allPages = format_tournament(self.data, string)
    await interaction.response.send_message(embed=allPages[0], view=ButtonView(create_initial_buttons(allPages, self.author), self.author), ephemeral=True)

class SelectView(discord.ui.View):
  def __init__(self, options, data, team_or_tournament_called, author, *, timeout = 180):
    try:
      super().__init__(timeout=timeout)
      self.add_item(Select(options, data, team_or_tournament_called, author))
    except Exception as e:
      print(e)