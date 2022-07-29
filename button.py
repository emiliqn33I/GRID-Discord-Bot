import discord

class Button(discord.ui.Button):
  def __init__(self, author, allPages, currPage, buttons, label, style, disabled, custom_id):
    super().__init__(label=label, style=style, disabled=disabled, custom_id=custom_id)
    self.author = author
    self.allPages = allPages
    self.buttons = buttons
    self.currPage = currPage
  async def callback(self, interaction):
    if(self.custom_id == "first_button"):
      # change page label to 1
      for i in self.buttons:
        self.buttons[i].currPage = 0
      self.buttons["page_button"].label = "1/" + str(len(self.allPages)) 

      # disable first and previous
      self.disabled = True
      self.buttons["prev_button"].disabled = True
      
      # enable next and last
      self.buttons["next_button"].disabled = False
      if(len(self.allPages) != 2):
        self.buttons["last_button"].disabled = False
    elif(self.custom_id == "prev_button"):
      # change page_button label
      for i in self.buttons:
        self.buttons[i].currPage -= 1
      self.buttons["page_button"].label = str(self.buttons[i].currPage + 1) + "/" + str(len(self.allPages))

      # disable previous if at first page
      if(self.currPage == 0):
        self.disabled = True
      
      # disable first if at second page
      if(self.currPage == 1):
        self.buttons["first_button"].disabled = True

      # enable next if at allPages[len-2]
      if(self.currPage == (len(self.allPages) - 2)):
        self.buttons["next_button"].disabled = False

      # enable last if at allPages[len-3]
      if(self.currPage == (len(self.allPages) - 3) and len(self.allPages) != 2):
        self.buttons["last_button"].disabled = False

    elif(self.custom_id == "next_button"):
      # change page_button label
      for i in self.buttons:
        self.buttons[i].currPage += 1
      self.buttons["page_button"].label = str(self.buttons[i].currPage + 1) + "/" + str(len(self.allPages))
      
      # disable next if at last page
      if(self.currPage == (len(self.allPages) - 1)):
        self.disabled = True

      # disable last if at allPages[len - 2]
      if(self.currPage == (len(self.allPages) - 2)):
        self.buttons["last_button"].disabled = True

      # enable previous if at allPages[1]
      if(self.currPage == 1):
        self.buttons["prev_button"].disabled = False
      
      # enable first if at allPages[2]
      if(self.currPage == 2 and len(self.allPages) != 2):
        self.buttons["first_button"].disabled = False
    elif(self.custom_id == "last_button"):
      # change page_button label to last
      for i in self.buttons:
        self.buttons[i].currPage = (len(self.allPages) - 1)
      self.buttons["page_button"].label = str(len(self.allPages)) + "/" + str(len(self.allPages))

      # disable last and next
      self.disabled = True
      self.buttons["next_button"].disabled = True

      # enable first and previous
      self.buttons["prev_button"].disabled = False
      if(len(self.allPages) != 2):
        self.buttons["first_button"].disabled = False
      
    await interaction.response.edit_message(embed=self.allPages[self.currPage], view=ButtonView(self.buttons, self.author))

class ButtonView(discord.ui.View):
  def __init__(self, buttons, author, *, timeout = 180):
    try:
      super().__init__(timeout=timeout)
      for i in buttons:
        self.add_item(buttons[i])
      self.author = author
      self.buttons = buttons
    except:
      pass
  async def interaction_check(self, interaction: discord.Interaction):
    return interaction.user.id == self.author.id

def create_initial_buttons(allPages, author):
  next_button_disabled = False
  last_button_disabled = False
  if(len(allPages) == 1):
    next_button_disabled = True
    last_button_disabled = True
  elif(len(allPages) == 2):
    last_button_disabled = True

  buttons = dict()

  buttons["first_button"] = Button(author, allPages, 0, buttons, "First", discord.ButtonStyle.primary, True, "first_button")
  buttons["prev_button"] = Button(author, allPages, 0, buttons, "Previous", discord.ButtonStyle.primary, True, "prev_button")
  buttons["page_button"] = Button(author, allPages, 0, buttons, ("1" + "/" + str(len(allPages))), discord.ButtonStyle.secondary, True, "page_button")
  buttons["next_button"] = Button(author, allPages, 0, buttons, "Next", discord.ButtonStyle.primary, next_button_disabled, "next_button")
  buttons["last_button"] = Button(author, allPages, 0, buttons, "Last", discord.ButtonStyle.primary, last_button_disabled, "last_button")

  return buttons